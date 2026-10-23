"""Week 2 lab, step 2: count tokens for the same paragraph in Turkish and English.

Three tokenizers: OpenAI tiktoken (o200k_base = GPT-4o/5/6 vocabulary),
a Qwen tokenizer and the Kumru (Turkish-first) tokenizer from Hugging Face.
Only tokenizer files are downloaded (a few MB), never model weights.
"""
import tiktoken

TR = (
    "Kiracı, kira bedelini her ayın en geç 5'inci gününe kadar kiraya verenin "
    "bildirdiği banka hesabına yatırmakla yükümlüdür. Geç ödeme hâlinde aylık %2 "
    "gecikme faizi uygulanır; üç ay üst üste geç ödeme, kiraya verene sözleşmeyi "
    "tek taraflı fesih hakkı verir. Kiracı, taşınmazı özenle kullanmak ve olağan "
    "bakım giderlerini karşılamakla yükümlüdür."
)
EN = (
    "The tenant must pay the rent into the bank account notified by the landlord "
    "no later than the 5th day of each month. In case of late payment, a monthly "
    "late-payment interest of 2% applies; three consecutive late payments give the "
    "landlord the right to terminate the contract unilaterally. The tenant must use "
    "the property with care and cover ordinary maintenance costs."
)

HF_TOKENIZERS = {
    "Qwen": "Qwen/Qwen3-0.6B",     # any Qwen3.x checkpoint shares this tokenizer
    "Kumru": "vngrs/Kumru-2B",     # Turkish-first vocabulary
}


def count_tiktoken(text: str, enc: str = "o200k_base") -> int:
    return len(tiktoken.get_encoding(enc).encode(text))


def count_hf(text: str, repo: str) -> int:
    from transformers import AutoTokenizer  # imported lazily: heavy

    tok = AutoTokenizer.from_pretrained(repo)
    return len(tok.encode(text, add_special_tokens=False))


if __name__ == "__main__":
    rows = [("tiktoken o200k", count_tiktoken(TR), count_tiktoken(EN))]
    for name, repo in HF_TOKENIZERS.items():
        try:
            rows.append((name, count_hf(TR, repo), count_hf(EN, repo)))
        except Exception as e:  # campus Wi-Fi may block huggingface.co
            print(f"skipping {name} ({repo}): {type(e).__name__}: {e}")

    print(f"\nwords: TR={len(TR.split())}  EN={len(EN.split())}\n")
    print(f"{'tokenizer':16} {'TR':>5} {'EN':>5} {'TR/EN':>6}")
    for name, tr, en in rows:
        print(f"{name:16} {tr:5d} {en:5d} {tr / en:6.2f}")

    # Try it: which single Turkish word explodes into the most tokens?
    enc = tiktoken.get_encoding("o200k_base")
    for w in ["Merhaba", "evlerimizdekilerden", "gelemeyeceklermiş", "İstanbul"]:
        print(f"{w:22} -> {len(enc.encode(w))} tokens: {[enc.decode([t]) for t in enc.encode(w)]}")
