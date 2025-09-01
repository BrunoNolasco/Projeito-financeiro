from typing import Optional, List, Dict, Any
from datetime import datetime
from mysql.connector import Error
from framework.db import get_connection

# Convenções assumidas de esquema:
# - Tabela `usuarios` (id INT PK, nome, email, ...).
# - Tabela `banco` (id INT PK, usuario_id INT FK, saldo DECIMAL(12,2)).
# - Tabela `transacoes` (id INT PK, usuario_id INT FK, tipo ENUM('deposito','retirada'),
#                       valor DECIMAL(12,2), descricao VARCHAR, data DATETIME).
#
# Se os nomes diferirem no seu BD, ajuste os SQLs abaixo.

def _normalize_decimal(valor: Any) -> float:
    if isinstance(valor, str):
        valor = valor.replace(",", ".").strip()
    return float(valor)

# --------------- SALDO ----------------
def get_saldo(usuario_id: int) -> float:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT saldo FROM banco WHERE usuario_id=%s", (usuario_id,))
            row = cur.fetchone()
            return float(row[0]) if row and row[0] is not None else 0.0
    finally:
        conn.close()

def _set_saldo(usuario_id: int, novo_saldo: float) -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO banco (usuario_id, saldo)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE saldo=VALUES(saldo)
            """, (usuario_id, novo_saldo))
        conn.commit()
    finally:
        conn.close()

# --------------- TRANSACOES ----------------
def add_transacao(usuario_id: int, tipo: str, valor: Any, descricao: str = "") -> Dict[str, Any]:
    tipo = tipo.lower().strip()
    if tipo not in ("deposito", "retirada"):
        return {"ok": False, "erro": "tipo inválido. Use 'deposito' ou 'retirada'."}

    try:
        v = _normalize_decimal(valor)
        if v <= 0:
            return {"ok": False, "erro": "valor deve ser > 0"}
    except Exception:
        return {"ok": False, "erro": "valor inválido"}

    saldo_atual = get_saldo(usuario_id)
    novo_saldo = saldo_atual + v if tipo == "deposito" else saldo_atual - v
    if novo_saldo < 0:
        return {"ok": False, "erro": "saldo insuficiente"}

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO transacoes (usuario_id, tipo, valor, descricao, data)
                VALUES (%s, %s, %s, %s, %s)
            """, (usuario_id, tipo, v, descricao, datetime.now()))
        conn.commit()
        _set_saldo(usuario_id, novo_saldo)
        return {"ok": True, "saldo": novo_saldo}
    except Error as e:
        return {"ok": False, "erro": str(e)}
    finally:
        conn.close()

def listar_transacoes(usuario_id: int, limite: int = 5) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT id, tipo, valor, descricao, data
                FROM transacoes
                WHERE usuario_id=%s
                ORDER BY data DESC, id DESC
                LIMIT %s
            """, (usuario_id, limite))
            rows = cur.fetchall() or []
            return [
                {
                    "id": r["id"],
                    "tipo": r["tipo"],
                    "valor": float(r["valor"]),
                    "descricao": r.get("descricao") or "",
                    "data": r["data"].strftime("%Y-%m-%d %H:%M:%S") if isinstance(r["data"], datetime) else str(r["data"]),
                }
                for r in rows
            ]
    finally:
        conn.close()

def editar_transacao(usuario_id: int, transacao_id: int, novo_tipo: Optional[str] = None,
                     novo_valor: Optional[Any] = None, nova_descricao: Optional[str] = None) -> Dict[str, Any]:
    
    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT id, tipo, valor
                FROM transacoes
                WHERE id=%s AND usuario_id=%s
            """, (transacao_id, usuario_id))
            row = cur.fetchone()
            if not row:
                return {"ok": False, "erro": "transação não encontrada"}

            tipo_atual = row["tipo"]
            valor_atual = float(row["valor"])

            
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

            
            saldo = get_saldo(usuario_id)
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
            if novo_tipo:
                sets.append("tipo=%s")
                params.append(tipo_final)
            if novo_valor is not None:
                sets.append("valor=%s")
                params.append(valor_final)
            if nova_descricao is not None:
                sets.append("descricao=%s")
                params.append(nova_descricao)

            if not sets:
                return {"ok": True, "saldo": saldo}

            params.extend([transacao_id, usuario_id])

            with conn.cursor() as cur2:
                cur2.execute(f"""
                    UPDATE transacoes
                    SET {", ".join(sets)}
                    WHERE id=%s AND usuario_id=%s
                """, tuple(params))
            conn.commit()
            _set_saldo(usuario_id, saldo)
            return {"ok": True, "saldo": saldo}
    finally:
        conn.close()

def excluir_transacao(usuario_id: int, transacao_id: int) -> Dict[str, Any]:
    
    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT id, tipo, valor
                FROM transacoes
                WHERE id=%s AND usuario_id=%s
            """, (transacao_id, usuario_id))
            row = cur.fetchone()
            if not row:
                return {"ok": False, "erro": "transação não encontrada"}

            tipo = row["tipo"]
            valor = float(row["valor"])

            
            saldo = get_saldo(usuario_id)
            if tipo == "deposito":
                saldo -= valor
            else:
                saldo += valor
            if saldo < 0:
                saldo = 0.0

            with conn.cursor() as cur2:
                cur2.execute("DELETE FROM transacoes WHERE id=%s AND usuario_id=%s", (transacao_id, usuario_id))
            conn.commit()
            _set_saldo(usuario_id, saldo)
            return {"ok": True, "saldo": saldo}
    finally:
        conn.close()

# --------------- PERFIL/CONTA ----------------
def get_perfil(usuario_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("SELECT id, nome, email FROM usuarios WHERE id=%s", (usuario_id,))
            row = cur.fetchone()
            return dict(row) if row else None
    finally:
        conn.close()

def atualizar_perfil(usuario_id: int, nome: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
    sets = []
    params: List[Any] = []
    if nome is not None:
        sets.append("nome=%s")
        params.append(nome)
    if email is not None:
        sets.append("email=%s")
        params.append(email)
    if not sets:
        return {"ok": True}

    conn = get_connection()
    try:
        params.extend([usuario_id])
        with conn.cursor() as cur:
            cur.execute(f"UPDATE usuarios SET {', '.join(sets)} WHERE id=%s", tuple(params))
        conn.commit()
        return {"ok": True}
    except Error as e:
        return {"ok": False, "erro": str(e)}
    finally:
        conn.close()

def excluir_conta(usuario_id: int) -> Dict[str, Any]:
    
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM transacoes WHERE usuario_id=%s", (usuario_id,))
            cur.execute("DELETE FROM banco WHERE usuario_id=%s", (usuario_id,))
            cur.execute("DELETE FROM usuarios WHERE id=%s", (usuario_id,))
        conn.commit()
        return {"ok": True}
    except Error as e:
        return {"ok": False, "erro": str(e)}
    finally:
        conn.close()
