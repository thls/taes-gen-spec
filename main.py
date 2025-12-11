# main.py
# ================================================================
# 1) Dependências e configuração
# ================================================================
import os
import json
import requests
import time
from pathlib import Path

import torch
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

try:
    # Disponível apenas em ambiente Colab
    from google.colab import userdata  # type: ignore
except ModuleNotFoundError:
    userdata = None


load_dotenv()

AI_API_KEY = os.getenv("AI_API_KEY")

# Modelo semântico baseado em RoBERTa Large
model = SentenceTransformer("stsb-roberta-large")

# ================================================================
# 2) Caminhos dos arquivos
#    (ajuste se o main.py não estiver na raiz do projeto)
# ================================================================
BASE_DIR = Path(__file__).resolve()
GOAL_DIR = Path("./goal")


# ================================================================
# 3) Util: carregar dataset_part
# ================================================================
def load_dataset_file(path: Path):
    with open(path, "r") as f:
        data = json.load(f)
    return data.get("dataset_part", [])


def load_all_goal_examples(goal_dir: Path) -> list:
    """Carrega e concatena todos os dataset_part dos JSON em goal_dir."""
    all_examples: list = []
    for json_path in sorted(goal_dir.glob("*.json")):
        examples = load_dataset_file(json_path)
        all_examples.extend(examples)
    return all_examples


# ================================================================
# 4) Funções de representação textual (por tipo de tag)
#    Agora retornam dicts no formato canônico para cada TAG.
# ================================================================
def build_paramtag_text(method_example, param_tag):
    sig = method_example.get("signature", "")
    cls = method_example.get("class", "")
    method_name = method_example.get("method", "")
    parameters = method_example.get("parameters", [])
    doc = method_example.get("doc", "")

    p_name = param_tag.get("parameter", '')
    comment = param_tag.get("comment", "")
    p_type = ''

    # Encontra o tipo do parâmetro
    for p in parameters:
        if p.get("name") == p_name:
            p_type = p.get("type", "")
            break

    return {
        "tag_type": "PARAM",
        "doc": doc,
        "signature": sig,
        "class": cls,
        "method": method_name,
        "param_name": p_name,
        "param_type": p_type,
        "comment": comment,
    }


def build_returntag_text(method_example, return_tag):
    sig = method_example.get("signature", "")
    cls = method_example.get("class", "")
    method_name = method_example.get("method", "")
    comment = return_tag.get("comment", "")
    r_type = method_example.get("returnType", "")
    doc = method_example.get("doc", "")

    return {
        "tag_type": "RETURN",
        "doc": doc,
        "signature": sig,
        "class": cls,
        "method": method_name,
        "return_type": r_type,
        "comment": comment
    }


def build_throwstag_text(method_example, throws_tag):
    sig = method_example.get("signature", "")
    cls = method_example.get("class", "")
    method_name = method_example.get("method", "")
    ex_type = throws_tag.get("exceptionType", '')
    comment = throws_tag.get("comment", "")
    doc = method_example.get("doc", "")
    return {
        "tag_type": "THROWS",
        "doc": doc,
        "signature": sig,
        "class": cls,
        "method": method_name,
        "exception_type": ex_type,
        "comment": comment
    }


# ================================================================
# 5) Embeddings dos GOAL por tipo
#    (remove "condition" e converte o dict para string)
# ================================================================
def compute_embeddings(examples: list):
    if not examples:
        return None

    cleaned = []
    for e in examples:
        d = e.copy()
        d.pop("condition", None)
        cleaned.append(str(d))

    return model.encode(cleaned, convert_to_tensor=True)


def format_log_entries(entries: list[dict], title: str) -> str:
    """
    Converte uma lista de entradas de log em texto simples.
    Inclui índices, assinatura, gabarito, predição, acerto e prompt usado.
    """
    lines = [title]
    for item in entries:
        lines.append(f"Index: {item.get('index')}")
        lines.append(f"Signature: {item.get('signature')}")
        lines.append(f"Ground truth: {item.get('ground_truth')}")
        lines.append(f"Predicted: {item.get('predicted_condition')}")
        lines.append(f"Correct: {item.get('correct')}")
        lines.append("Prompt:")
        lines.append(item.get("prompt", ""))
        lines.append("-" * 40)
    return "\n".join(lines)


def print_progress(label: str, current: int, total: int):
    """Mostra progresso simples no stdout."""
    if total <= 0:
        return
    pct = (current / total) * 100
    print(f"[{label}] {current}/{total} ({pct:.1f}%)", flush=True)


# ================================================================
# 6) Função para pegar top-k similares
# ================================================================
def top_k_similar(
    test_tag_wo_cond: dict,
    goal_examples: list,
    goal_emb,
    k: int = 10,
    exclude_index: int | None = None,
):
    """
    test_tag_wo_cond: dict (sem campo 'condition')
    goal_examples: lista de dicts (com 'condition')
    goal_emb: tensor [N, D] dos goal_examples
    exclude_index: índice (int) do exemplo que queremos excluir da busca
    A busca também exclui exemplos do mesmo método (signature ou par classe+method).
    """
    if goal_emb is None or not goal_examples:
        return []

    # Gera embedding do exemplo de teste a partir do dict sem 'condition'
    test_dict = test_tag_wo_cond.copy()
    test_dict.pop("condition", None)
    test_text = str(test_dict)

    test_emb = model.encode([test_text], convert_to_tensor=True)
    scores = util.pytorch_cos_sim(test_emb, goal_emb)[0]  # [N]

    # Exclui a própria posição m (oráculo) e qualquer exemplo do mesmo método
    same_sig = test_tag_wo_cond.get("signature")
    same_class = test_tag_wo_cond.get("class")
    same_method = test_tag_wo_cond.get("method")

    invalid_mask = []
    for i, ex in enumerate(goal_examples):
        invalid = False
        if exclude_index is not None and i == exclude_index:
            invalid = True
        ex_sig = ex.get("signature")
        ex_class = ex.get("class")
        ex_method = ex.get("method")
        if same_sig and ex_sig == same_sig:
            invalid = True
        elif (
            same_class
            and same_method
            and ex_class == same_class
            and ex_method == same_method
        ):
            invalid = True
        invalid_mask.append(invalid)

    valid_count = len([v for v in invalid_mask if not v])
    if valid_count <= 0:
        return []

    mask_tensor = torch.tensor(invalid_mask, device=scores.device)
    scores = scores.masked_fill(mask_tensor, -1e9)

    # Número efetivo de vizinhos
    k_eff = min(k, valid_count)
    if k_eff <= 0:
        return []

    topk = torch.topk(scores, k_eff)
    indices = topk.indices.tolist()

    return [goal_examples[i] for i in indices]


# ================================================================
# 7) Few-shot prompt builder genérico
# ================================================================
def build_fewshot_prompt(
    tag_kind: str, similar_goal_tags: list[dict], test_tag_without_cond: dict
) -> str:
    """
    tag_kind: "PARAM", "RETURN" ou "THROWS"
    similar_goal_tags: lista de dicts (do GOAL) com campo 'condition'
    test_tag_without_cond: dict (no mesmo formato, mas sem 'condition')
    """
    prompt = (
        f"You infer Ruby boolean conditions for {tag_kind} tags "
        f"in Ruby YARD-style documentation.\n\n"
    )

    tag_label = f"{tag_kind} TAG"

    # Exemplos de few-shot
    for g in similar_goal_tags:
        cond = g.get("condition", "")

        # Não queremos que a condition apareça no JSON de exemplo
        tag_no_cond = {k: v for k, v in g.items() if k != "condition"}

        prompt += f"""
### Example
{tag_label}:
{json.dumps(tag_no_cond, indent=2)}

Correct condition:
{cond}
--------------------------------------------------
"""

    # Exemplo alvo (sem condition)
    prompt += f"""
### Target {tag_label} (predict the condition)

{tag_label}:
{json.dumps(test_tag_without_cond, indent=2)}

Task:
Infer the correct Ruby boolean expression for the field "condition" of this {tag_label}.
Return ONLY the condition string, without explanation, without quotes.
"""
    return prompt


# ================================================================
# 9) Chamada à LLM via Ollama Cloud
# ================================================================
def call_llm(prompt: str, max_retries: int = 3, wait_seconds: int = 60) -> str:
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "ministral-3:14b",  # modelo da sua lista
        "prompt": prompt,
        "stream": False,  # queremos a resposta inteira de uma vez
    }

    headers = {
        # "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
    }

    last_error: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(url, json=payload, headers=headers)
            resp.raise_for_status()  # levanta erro se vier 4xx/5xx
            data = resp.json()
            predicted_text = data.get("response", "")
            return predicted_text.strip()
        except requests.HTTPError as exc:
            last_error = exc
            status = exc.response.status_code if exc.response is not None else None
            if status == 429 and attempt < max_retries:
                print(
                    f"[LLM] 429 recebido (tentativa {attempt}/{max_retries}), "
                    f"aguardando {wait_seconds}s antes de tentar novamente...",
                    flush=True,
                )
                time.sleep(wait_seconds)
                continue
            raise
        except requests.RequestException as exc:
            last_error = exc
            if attempt < max_retries:
                print(
                    f"[LLM] Erro de requisição (tentativa {attempt}/{max_retries}), "
                    f"aguardando {wait_seconds}s antes de tentar novamente...",
                    flush=True,
                )
                time.sleep(wait_seconds)
                continue
            raise

    # Só chega aqui se todas as tentativas falharem e a exceção não for levantada
    if last_error:
        raise last_error


# ================================================================
# 10) Função principal
# ================================================================
def main():
    # ---------------- Carregar exemplos GOAL ----------------
    goal_examples = load_all_goal_examples(GOAL_DIR)
    print(f"Loaded {len(goal_examples)} goal methods from {GOAL_DIR}")

    # ---------------- Flatten por tipo de TAG ----------------
    goal_param_tags: list[dict] = []
    goal_return_tags: list[dict] = []
    goal_throws_tags: list[dict] = []

    for ex in goal_examples:
        # PARAM
        for pt in ex.get("paramTags", []):
            cond = pt.get("condition")
            if cond:
                txt = build_paramtag_text(ex, pt)
                txt["condition"] = cond
                goal_param_tags.append(txt)

        # RETURN (note que agora usamos "returnTags" no dataset)
        for rt in ex.get("returnTags", []):
            cond = rt.get("condition")
            if cond:
                txt = build_returntag_text(ex, rt)
                txt["condition"] = cond
                goal_return_tags.append(txt)

        # THROWS
        for tt in ex.get("throwsTags", []):
            cond = tt.get("condition")
            if cond:
                txt = build_throwstag_text(ex, tt)
                txt["condition"] = cond
                goal_throws_tags.append(txt)

    print("Goal PARAM tags :", len(goal_param_tags))
    print("Goal RETURN tags:", len(goal_return_tags))
    print("Goal THROWS tags:", len(goal_throws_tags))

    # ---------------- Embeddings por tipo ----------------
    goal_param_emb = compute_embeddings(goal_param_tags)
    goal_return_emb = compute_embeddings(goal_return_tags)
    goal_throws_emb = compute_embeddings(goal_throws_tags)

    if goal_param_emb is not None:
        print("PARAM embedding shape :", goal_param_emb.shape)
    if goal_return_emb is not None:
        print("RETURN embedding shape:", goal_return_emb.shape)
    if goal_throws_emb is not None:
        print("THROWS embedding shape:", goal_throws_emb.shape)

    # ============================================================
    # LOOP 1 — PARAM TAGS + métricas
    # ============================================================
    param_results = []
    param_gold_count = len(goal_param_tags)
    param_correct_count = 0

    param_success_logs = []
    param_error_logs = []
    for index, m in enumerate(goal_param_tags):
        ground_truth = m.get("condition")

        test_tag_without_cond = m.copy()
        test_tag_without_cond.pop("condition", None)

        similars = top_k_similar(
            test_tag_wo_cond=test_tag_without_cond,
            goal_examples=goal_param_tags,
            goal_emb=goal_param_emb,
            k=10,  # ajuste conforme o experimento
            exclude_index=index,
        )

        prompt = build_fewshot_prompt("PARAM", similars, test_tag_without_cond)

        predicted = call_llm(prompt)

        correct = (ground_truth is not None and predicted == ground_truth)

        if correct:
            param_correct_count += 1

        result_entry = {
            "type": "PARAM",
            "index": index,
            "signature": m.get("signature", ""),
            "tag": m,
            "ground_truth": ground_truth,
            "predicted_condition": predicted,
            "correct": correct,
            "prompt": prompt,
        }

        param_results.append(result_entry)
        if correct:
            param_success_logs.append(result_entry)
        else:
            param_error_logs.append(result_entry)

        print_progress("PARAM", index + 1, param_gold_count)

    param_accuracy = (
        param_correct_count / param_gold_count if param_gold_count > 0 else 0.0
    )

    # ============================================================
    # LOOP 2 — RETURN TAGS + métricas
    # ============================================================
    return_results = []
    return_gold_count = len(goal_return_tags)
    return_correct_count = 0

    return_success_logs = []
    return_error_logs = []
    for index, m in enumerate(goal_return_tags):
        ground_truth = m.get("condition")

        test_tag_without_cond = m.copy()
        test_tag_without_cond.pop("condition", None)

        similars = top_k_similar(
            test_tag_wo_cond=test_tag_without_cond,
            goal_examples=goal_return_tags,
            goal_emb=goal_return_emb,
            k=10,
            exclude_index=index,
        )

        prompt = build_fewshot_prompt("RETURN", similars, test_tag_without_cond)

        predicted = call_llm(prompt)

        correct = (ground_truth is not None and predicted == ground_truth)

        if correct:
            return_correct_count += 1

        result_entry = {
            "type": "RETURN",
            "index": index,
            "signature": m.get("signature", ""),
            "tag": m,
            "ground_truth": ground_truth,
            "predicted_condition": predicted,
            "correct": correct,
            "prompt": prompt,
        }

        return_results.append(result_entry)
        if correct:
            return_success_logs.append(result_entry)
        else:
            return_error_logs.append(result_entry)

        print_progress("RETURN", index + 1, return_gold_count)

    return_accuracy = (
        return_correct_count / return_gold_count if return_gold_count > 0 else 0.0
    )

    # ============================================================
    # LOOP 3 — THROWS TAGS + métricas
    # ============================================================
    throws_results = []
    throws_gold_count = len(goal_throws_tags)
    throws_correct_count = 0

    throws_success_logs = []
    throws_error_logs = []
    for index, m in enumerate(goal_throws_tags):
        ground_truth = m.get("condition")

        test_tag_without_cond = m.copy()
        test_tag_without_cond.pop("condition", None)

        similars = top_k_similar(
            test_tag_wo_cond=test_tag_without_cond,
            goal_examples=goal_throws_tags,
            goal_emb=goal_throws_emb,
            k=10,
            exclude_index=index,
        )

        prompt = build_fewshot_prompt("THROWS", similars, test_tag_without_cond)

        predicted = call_llm(prompt)

        correct = (ground_truth is not None and predicted == ground_truth)

        if correct:
            throws_correct_count += 1

        result_entry = {
            "type": "THROWS",
            "index": index,
            "signature": m.get("signature", ""),
            "tag": m,
            "ground_truth": ground_truth,
            "predicted_condition": predicted,
            "correct": correct,
            "prompt": prompt,
        }

        throws_results.append(result_entry)
        if correct:
            throws_success_logs.append(result_entry)
        else:
            throws_error_logs.append(result_entry)

        print_progress("THROWS", index + 1, throws_gold_count)

    throws_accuracy = (
        throws_correct_count / throws_gold_count if throws_gold_count > 0 else 0.0
    )

    # ============================================================
    # 13) MÉTRICAS GERAIS
    # ============================================================
    total_examples = param_gold_count + return_gold_count + throws_gold_count
    total_correct = param_correct_count + return_correct_count + throws_correct_count
    overall_accuracy = total_correct / total_examples if total_examples > 0 else 0.0

    all_results = {
        "param_results": param_results,
        "return_results": return_results,
        "throws_results": throws_results,
        "metrics": {
            "param": {
                "gold": param_gold_count,
                "correct": param_correct_count,
                "accuracy": param_accuracy,
            },
            "return": {
                "gold": return_gold_count,
                "correct": return_correct_count,
                "accuracy": return_accuracy,
            },
            "throws": {
                "gold": throws_gold_count,
                "correct": throws_correct_count,
                "accuracy": throws_accuracy,
            },
            "overall": {
                "gold": total_examples,
                "correct": total_correct,
                "accuracy": overall_accuracy,
            },
        },
    }

    # Salva resultados em JSON na raiz do projeto
    results_path = './results.json'
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2)

    # Logs detalhados por tipo de TAG
    logs_paths = {
        "param_success_json": "./param_success_logs.json",
        "param_error_json": "./param_error_logs.json",
        "return_success_json": "./return_success_logs.json",
        "return_error_json": "./return_error_logs.json",
        "throws_success_json": "./throws_success_logs.json",
        "throws_error_json": "./throws_error_logs.json",
        "param_success_txt": "./param_success_logs.txt",
        "param_error_txt": "./param_error_logs.txt",
        "return_success_txt": "./return_success_logs.txt",
        "return_error_txt": "./return_error_logs.txt",
        "throws_success_txt": "./throws_success_logs.txt",
        "throws_error_txt": "./throws_error_logs.txt",
        "metrics_txt": "./results_summary.txt",
    }

    # JSON
    with open(logs_paths["param_success_json"], "w") as f:
        json.dump(param_success_logs, f, indent=2)
    with open(logs_paths["param_error_json"], "w") as f:
        json.dump(param_error_logs, f, indent=2)

    with open(logs_paths["return_success_json"], "w") as f:
        json.dump(return_success_logs, f, indent=2)
    with open(logs_paths["return_error_json"], "w") as f:
        json.dump(return_error_logs, f, indent=2)

    with open(logs_paths["throws_success_json"], "w") as f:
        json.dump(throws_success_logs, f, indent=2)
    with open(logs_paths["throws_error_json"], "w") as f:
        json.dump(throws_error_logs, f, indent=2)

    # TXT (plain text)
    with open(logs_paths["param_success_txt"], "w") as f:
        f.write(format_log_entries(param_success_logs, "PARAM SUCCESS LOGS"))
    with open(logs_paths["param_error_txt"], "w") as f:
        f.write(format_log_entries(param_error_logs, "PARAM ERROR LOGS"))

    with open(logs_paths["return_success_txt"], "w") as f:
        f.write(format_log_entries(return_success_logs, "RETURN SUCCESS LOGS"))
    with open(logs_paths["return_error_txt"], "w") as f:
        f.write(format_log_entries(return_error_logs, "RETURN ERROR LOGS"))

    with open(logs_paths["throws_success_txt"], "w") as f:
        f.write(format_log_entries(throws_success_logs, "THROWS SUCCESS LOGS"))
    with open(logs_paths["throws_error_txt"], "w") as f:
        f.write(format_log_entries(throws_error_logs, "THROWS ERROR LOGS"))

    # Resumo em texto simples
    metrics_lines = [
        "RESULTS SUMMARY",
        f"Total gold examples: {total_examples}",
        f"Total correct: {total_correct}",
        f"Overall accuracy: {overall_accuracy}",
        "",
        "PARAM:",
        f"  Gold: {param_gold_count}",
        f"  Correct: {param_correct_count}",
        f"  Accuracy: {param_accuracy}",
        "",
        "RETURN:",
        f"  Gold: {return_gold_count}",
        f"  Correct: {return_correct_count}",
        f"  Accuracy: {return_accuracy}",
        "",
        "THROWS:",
        f"  Gold: {throws_gold_count}",
        f"  Correct: {throws_correct_count}",
        f"  Accuracy: {throws_accuracy}",
    ]
    with open(logs_paths["metrics_txt"], "w") as f:
        f.write("\n".join(metrics_lines))

    print(f"\nResultados salvos em: {results_path}")
    print("Logs JSON:")
    print(f"  PARAM sucesso : {logs_paths['param_success_json']}")
    print(f"  PARAM erro    : {logs_paths['param_error_json']}")
    print(f"  RETURN sucesso: {logs_paths['return_success_json']}")
    print(f"  RETURN erro   : {logs_paths['return_error_json']}")
    print(f"  THROWS sucesso: {logs_paths['throws_success_json']}")
    print(f"  THROWS erro   : {logs_paths['throws_error_json']}")
    print("Logs TXT:")
    print(f"  PARAM sucesso : {logs_paths['param_success_txt']}")
    print(f"  PARAM erro    : {logs_paths['param_error_txt']}")
    print(f"  RETURN sucesso: {logs_paths['return_success_txt']}")
    print(f"  RETURN erro   : {logs_paths['return_error_txt']}")
    print(f"  THROWS sucesso: {logs_paths['throws_success_txt']}")
    print(f"  THROWS erro   : {logs_paths['throws_error_txt']}")
    print(f"Resumo TXT      : {logs_paths['metrics_txt']}")


if __name__ == "__main__":
    main()
