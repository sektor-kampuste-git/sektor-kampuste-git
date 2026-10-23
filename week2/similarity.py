"""Week 2 lab, bonus: cosine similarity of 5 Turkish sentences with a Turkish embedding model.

pip install sentence-transformers   (downloads ~1 GB model on first run; use Colab if RAM is tight)
"""
from sentence_transformers import SentenceTransformer, util

MODEL = "ytu-ce-cosmos/turkish-e5-large"  # alternative: intfloat/multilingual-e5-base
SENTENCES = [
    "Faturamı nasıl öderim?",
    "Ödeme nasıl yapılır?",
    "Kargom ne zaman gelir?",
    "Siparişimin teslimat tarihi nedir?",
    "Hava bugün çok güzel.",
]

model = SentenceTransformer(MODEL)
# e5 models expect a "query: " prefix
emb = model.encode([f"query: {s}" for s in SENTENCES], normalize_embeddings=True)
sim = util.cos_sim(emb, emb)

print(f"{'':32}" + "".join(f"{i + 1:>7}" for i in range(len(SENTENCES))))
for i, s in enumerate(SENTENCES):
    print(f"{s[:30]:32}" + "".join(f"{sim[i][j]:7.2f}" for j in range(len(SENTENCES))))
print("\nWhich pairs are near 1? Which are near 0? That geometry is what RAG (Week 5) searches.")
