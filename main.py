
from fastapi import FastAPI, Request
import openai
import os

app = FastAPI()

openai.api_key = "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"

@app.post("/gerar-cardapio")
async def gerar_cardapio(request: Request):
    data = await request.json()
    tdee = data.get("tdee")
    deficit = data.get("deficit", 30)
    alimentos = data.get("alimentos", {})

    calorias_alvo = round(tdee * (1 - deficit / 100))

    prompt = f"""
Você é um nutricionista. Crie um cardápio diário com aproximadamente {calorias_alvo} calorias, dividido em:
- Café da Manhã
- Lanche da Manhã
- Almoço
- Lanche da Tarde
- Jantar
- Ceia

Use apenas os seguintes alimentos:

{chr(10).join([f"- {refeicao}: {', '.join(itens)}" for refeicao, itens in alimentos.items()])}

Informe as calorias por refeição e o total final.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um nutricionista especialista em emagrecimento."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )

    cardapio = response.choices[0].message.content
    return {"cardapio": cardapio}
