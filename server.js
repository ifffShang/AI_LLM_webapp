// server.js
const express = require("express");
const dotenv = require("dotenv");
const cors = require("cors");
const bodyParser = require("body-parser");
const axios = require("axios");

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());

const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;
const MODEL = "deepseek/deepseek-chat-v3-0324:free";

app.get("/", (req, res) => {
  res.send("✅ Server is running");
});

app.post("/api/ask", async (req, res) => {
  const { query } = req.body;
  if (!query) return res.status(400).json({ error: "Missing query" });

  try {
    const response = await axios("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: MODEL,
        messages: [{ role: "user", content: query }],
      }),
    });

    const data = await response.json();

    if (!data.choices || !data.choices[0]?.message?.content) {
      return res.status(500).json({ error: "Invalid response from OpenRouter" });
    }

    const content = data.choices[0].message.content;
    const sections = content.split("\n\n").filter(Boolean);

    res.json({ sections });
  } catch (error) {
    console.error("/api/ask error:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
