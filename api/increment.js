import { promises as fs } from "fs";
import path from "path";

const countFile = path.join("/tmp", "count.txt");

export default async function handler(req, res) {
  // ✅ Add these CORS headers at the start
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  // ✅ Handle OPTIONS preflight request
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  // ✅ Your existing POST logic
  if (req.method === "POST") {
    try {
      let count = 0;
      try {
        const data = await fs.readFile(countFile, "utf8");
        count = parseInt(data) || 0;
      } catch {}

      count++;
      await fs.writeFile(countFile, count.toString());
      res.status(200).json({ success: true, count });
    } catch (e) {
      res.status(500).json({ success: false, error: e.message });
    }
  }

  // ✅ Your existing GET logic
  else if (req.method === "GET") {
    try {
      const data = await fs.readFile(countFile, "utf8");
      const count = parseInt(data) || 0;
      res.status(200).json({ count });
    } catch {
      res.status(200).json({ count: 0 });
    }
  }

  // ✅ Method not allowed
  else {
    res.status(405).json({ error: "Method not allowed" });
  }
}
