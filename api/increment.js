import { promises as fs } from "fs";
import path from "path";

// Use /tmp directory for writable file storage on Vercel
const countFile = path.join("/tmp", "count.txt");

export default async function handler(req, res) {
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
  } else if (req.method === "GET") {
    try {
      const data = await fs.readFile(countFile, "utf8");
      const count = parseInt(data) || 0;
      res.status(200).json({ count });
    } catch {
      // File doesn't exist yet or unreadable, so count is 0
      res.status(200).json({ count: 0 });
    }
  } else {
    res.status(405).json({ error: "Method not allowed" });
  }
}
