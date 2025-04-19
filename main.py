from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# Libera o CORS pra qualquer origem (ajuste depois pro seu domínio se quiser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dados recebidos do frontend
class CardapioRequest(BaseModel):
    tdee: int
    deficit: int
    alimentos: dict

@app.post("/gerar-cardapio")
async def gerar_cardapio(data: CardapioRequest):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    calorias_dia = data.tdee - data.deficit
    prompt = f"""
Crie um cardápio de um dia com aproximadamente {calorias_dia} calorias, dividido em:
- Café da manhã
- Lanche da manhã
- Almoço
- Lanche da tarde
- Jantar
- Ceia

Use somente os seguintes alimentos permitidos para cada refeição:
{data.alimentos}

Formato da resposta:
Café da Manhã:
- Alimento 1
- Alimento 2
(Quantidade aproximada em calorias: XXX kcal)

...

Total aproximado: XXXX kcal
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )

    cardapio_texto = response.choices[0].message.content
    return {"cardapio": cardapio_texto}
