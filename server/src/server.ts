import express, { Express, Request, Response } from "express";
import fs from "fs";
import path from "path";
import dotenv from "dotenv";
const app: Express = express();
dotenv.config();
const port: string | undefined = process.env.PORT || "3000";

// Serve Vue Build
app.use(express.static(path.join(__dirname, '../frontendDist')));

// Files
const distDir: string = path.join(__dirname, '../frontendDist');
const vueIndexFile: string = path.join(distDir, 'index.html');
const fallbackFile: string = path.join(__dirname, 'fallback.html');

// Catch All
app.get('*', (_req: Request, res: Response) => {
    const distExists: boolean = fs.existsSync(distDir);
    const indexExists: boolean = fs.existsSync(vueIndexFile);
    if (distExists && indexExists) {
        res.sendFile(path.resolve(__dirname, '../frontendDist', 'index.html'));
    } else res.sendFile(fallbackFile);
});

// Start
app.listen(port, async () => console.log(`Hosting server listening on port ${port}.`));
