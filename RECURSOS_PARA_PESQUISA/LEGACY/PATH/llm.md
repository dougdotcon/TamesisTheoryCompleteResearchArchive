api: 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

Responda em JSON:
{
  "problema_ainda_existe": true/false,
  "barreira_original": "tecnica | custo | regulatoria | mercado",
  "o_que_mudou_desde_entao": "...",
  "potencial_com_tecnologia_atual": 0-10,
  "possiveis_mercados_atuais": ["..."],
  "comentario_critico": "..."
}

import { OpenRouter } from "@openrouter/sdk";

const openrouter = new OpenRouter({
  apiKey: "<OPENROUTER_API_KEY>"
});

const stream = await openrouter.chat.send({
  model: "z-ai/glm-4.5-air:free",
  messages: [
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ],
  stream: true
});

for await (const chunk of stream) {
  const content = chunk.choices[0]?.delta?.content;
  if (content) {
    process.stdout.write(content);
  }
}
