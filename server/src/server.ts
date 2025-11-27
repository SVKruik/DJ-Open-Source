import express, { Express, Request, Response } from "express";
import fs from "fs";
import path from "path";
import shell from "shelljs";
import dotenv from "dotenv";
import { Channel, Message } from "amqplib";
import { getConnection } from "./connection";
import { UplinkMessage } from "./customTypes";
const app: Express = express();
dotenv.config();
const port: string | undefined = process.env.PORT;

// Status Shield
app.get("/api/status/badge", (_req: Request, res: Response) => {
    res.json({ "schemaVersion": 1, "label": "Site Status", "message": "online", "color": "brightgreen" });
});

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
app.listen(port, async () => {
    // Setup
    const channel: Channel | null = await getConnection();
    if (!channel) throw new Error("Uplink connection missing.");
    channel.assertExchange("unicast-misc", "direct", { durable: false });
    const queue = await channel.assertQueue("", { exclusive: true });
    await channel.bindQueue(queue.queue, "unicast-misc", "dj-open-source");

    // Listen
    channel.consume(queue.queue, (message: Message | null) => {
        if (message) {
            const messageContent: UplinkMessage = JSON.parse(message.content.toString());
            channel.ack(message);
            if (messageContent.task === "Deploy" && process.platform === "linux") {
                console.log(`Received new deploy task from ${messageContent.sender}. Running Server deployment script.`);
                shell.exec("bash deploy.sh");
            }
        }
    }, {
        noAck: false
    });
    console.log(`Hosting server listening on port ${port}.`);
});
