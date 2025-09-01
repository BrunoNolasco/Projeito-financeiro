from typing import Optional, List, Dict, Any
from datetime import datetime
from mysql.connector import Error
from db import get_connection

def _normalize_decimal(valor: Any) -> float:
    if isinstance(valor, str):
        valor = valor.replace(",", ".").strip()
    return float(valor)

# --------- CRIAR CONTA / AUTH ----------
def criar_conta_banco(nome: str, sobrenome: str, senha_plana: str, saldo_inicial: float,
                      nascimento: str, endereco: str, telefone: str, contribuinte: str):
    """
    Insere usuário na tabela banco e retorna (ok, msg).
    """
    import hashlib
    senha_hash = hashlib.sha256(senha_plana.encode('utf-8')).hexdigest()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO banco (nome, sobrenome, senha_hash, saldo, nascimento, endereco, telefone, contribuinte)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nome, sobrenome, senha_hash, saldo_inicial, nascimento, endereco, telefone, contribuinte))
        conn.commit()
        return True, "Conta criada com sucesso."
    except Error as e:
        return False, f"Erro ao criar conta: {e}"
    finally:
        conn.close()

def autenticar_usuario(nome: str, senha_plana: str) -> Optional[int]:
    """
    Retorna banco.id se as credenciais estiverem corretas.
    """
    import hashlib
    senha_hash = hashlib.sha256(senha_plana.encode('utf-8')).hexdigest()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM banco WHERE nome=%s AND senha_hash=%s", (nome, senha_hash))
            row = cur.fetchone()
            return int(row[0]) if row else None
    finally:
        conn.close()

# --------------- SALDO ----------------
def get_saldo(user_id: int) -> float:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT saldo FROM banco WHERE id=%s", (user_id,))
            row = cur.fetchone()
            return float(row[0]) if row and row[0] is not None else 0.0
    finally:
        conn.close()

def _set_saldo(user_id: int, novo_saldo: float) -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE banco SET saldo=%s WHERE id=%s", (novo_saldo, user_id))
        conn.commit()
    finally:
        conn.close()

# --------------- TRANSACOES ----------------
def add_transacao(user_id: int, tipo: str, valor: Any, descricao: str = "") -> Dict[str, Any]:
    tipo = tipo.lower().strip()
    if tipo not in ("deposito", "retirada"):
        return {"ok": False, "erro": "tipo inválido. Use 'deposito' ou 'retirada'."}

    try:
        v = _normalize_decimal(valor)
        if v <= 0:
            return {"ok": False, "erro": "valor deve ser > 0"}
    except Exception:
        return {"ok": False, "erro": "valor inválido"}

    saldo_atual = get_saldo(user_id)
    novo_saldo = saldo_atual + v if tipo == "deposito" else saldo_atual - v
    if novo_saldo < 0:
        return {"ok": False, "erro": "saldo insuficiente"}

    creditado = v if tipo == "deposito" else 0.0
    debitado = v if tipo == "retirada" else 0.0

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # requer colunas id e descricao (veja migração abaixo)
            cur.execute("""
                INSERT INTO transacao (creditado, debitado, descricao, id_banco, data)
                VALUES (%s, %s, %s, %s, NOW())
            """, (creditado, debitado, descricao, user_id))
        conn.commit()
        _set_saldo(user_id, novo_saldo)
        return {"ok": True, "saldo": novo_saldo}
    except Error as e:
        return {"ok": False, "erro": str(e)}
    finally:
        conn.close()

def listar_transacoes(user_id: int, limite: int = 10) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT id, creditado, debitado, descricao, data
                FROM transacao
                WHERE id_banco=%s
                ORDER BY data DESC, id DESC
                LIMIT %s
            """, (user_id, limite))
            rows = cur.fetchall() or []
            itens = []
            for r in rows:
                cred = float(r["creditado"] or 0)
                deb = float(r["debitado"] or 0)
                tipo = "deposito" if cred > 0 else "retirada"
                valor = cred if cred > 0 else deb
                itens.append({
                    "id": int(r["id"]),
                    "tipo": tipo,
                    "valor": valor,
                    "descricao": r.get("descricao") or "",
                    "data": r["data"].strftime("%Y-%m-%d %H:%M:%S") if isinstance(r["data"], datetime) else str(r["data"]),
                })
            return itens
    finally:
        conn.close()

def editar_transacao(user_id: int, transacao_id: int, novo_tipo: Optional[str] = None,
                     novo_valor: Optional[Any] = None, nova_descricao: Optional[str] = None) -> Dict[str, Any]:
    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT id, creditado, debitado
                FROM transacao
                WHERE id=%s AND id_banco=%s
            """, (transacao_id, user_id))
            row = cur.fetchone()
            if not row:
                return {"ok": False, "erro": "transação não encontrada"}

            cred_atual = float(row["creditado"] or 0)
            deb_atual = float(row["debitado"] or 0)
            tipo_atual = "deposito" if cred_atual > 0 else "retirada"
            valor_atual = cred_atual if cred_atual > 0 else deb_atual

            tipo_final = tipo_atual
            if novo_tipo:
                novo_tipo = novo_tipo.lower().strip()
                if novo_tipo not in ("deposito", "retirada"):
                    return {"ok": False, "erro": "tipo inválido"}
                tipo_final = novo_tipo

            valor_final = valor_atual
            if novo_valor is not None:
                try:
                    valor_final = _normalize_decimal(novo_valor)
                    if valor_final <= 0:
                        return {"ok": False, "erro": "valor deve ser > 0"}
                except Exception:
                    return {"ok": False, "erro": "valor inválido"}

            # desfaz antiga e aplica nova no saldo
            saldo = get_saldo(user_id)
            if tipo_atual == "deposito":
                saldo -= valor_atual
            else:
                saldo += valor_atual
            if tipo_final == "deposito":
                saldo += valor_final
            else:
                saldo -= valor_final
            if saldo < 0:
                return {"ok": False, "erro": "saldo insuficiente"}

            sets = []
            params: List[Any] = []
            if novo_tipo or novo_valor is not None:
                cred = valor_final if tipo_final == "deposito" else 0.0
                deb = valor_final if tipo_final == "retirada" else 0.0
                sets.append("creditado=%s")
                params.append(cred)
                sets.append("debitado=%s")
                params.append(deb)
            if nova_descricao is not None:
                sets.append("descricao=%s")
                params.append(nova_descricao)

            if not sets:
                return {"ok": True, "saldo": saldo}

            params.extend([transacao_id, user_id])

            with conn.cursor() as cur2:
                cur2.execute(f"""
                    UPDATE transacao
                    SET {", ".join(sets)}
                    WHERE id=%s AND id_banco=%s
                """, tuple(params))
            conn.commit()
            _set_saldo(user_id, saldo)
            return {"ok": True, "saldo": saldo}
    finally:
        conn.close()

def excluir_transacao(user_id: int, transacao_id: int) -> Dict[str, Any]:
    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT creditado, debitado
                FROM transacao
                WHERE id=%s AND id_banco=%s
            """, (transacao_id, user_id))
            row = cur.fetchone()
            if not row:
                return {"ok": False, "erro": "transação não encontrada"}

            cred = float(row["creditado"] or 0)
            deb = float(row["debitado"] or 0)
            valor = cred if cred > 0 else deb
            tipo = "deposito" if cred > 0 else "retirada"

            saldo = get_saldo(user_id)
            if tipo == "deposito":
                saldo -= valor
            else:
                saldo += valor
            if saldo < 0:
                saldo = 0.0

            with conn.cursor() as cur2:
                cur2.execute("DELETE FROM transacao WHERE id=%s AND id_banco=%s", (transacao_id, user_id))
            conn.commit()
            _set_saldo(user_id, saldo)
            return {"ok": True, "saldo": saldo}
    finally:
        conn.close()

# --------------- PERFIL/CONTA ----------------
def get_perfil(user_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("SELECT id, nome FROM banco WHERE id=%s", (user_id,))
            row = cur.fetchone()
            if not row:
                return None
            # 'email' não existe no esquema — devolve vazio só pra UI não quebrar
            return {"id": row["id"], "nome": row["nome"], "email": ""}
    finally:
        conn.close()

def atualizar_perfil(user_id: int, nome: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
    if nome is None:
        return {"ok": True}
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE banco SET nome=%s WHERE id=%s", (nome, user_id))
        conn.commit()
        return {"ok": True}
    except Error as e:
        return {"ok": False, "erro": str(e)}
    finally:
        conn.close()
