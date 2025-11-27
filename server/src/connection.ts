import amqp from "amqplib";
import dotenv from "dotenv";
import { Channel } from "amqplib";
dotenv.config();

let channel: Channel | null = null;
async function createConnection(): Promise<void> {
    try {
        const connection = await (await amqp.connect({
            "protocol": "amqp",
            "hostname": process.env.AMQP_HOST,
            "port": parseInt(process.env.AMQP_PORT as string),
            "username": process.env.AMQP_USERNAME,
            "password": process.env.AMQP_PASSWORD
        })).createChannel();
        channel = connection;
    } catch (error: any) {
        console.error(error);
    }
}

/**
 * Gets the existing or creates a new channel for working with Uplink.
 * @returns The RabbitMQ Channel
 */
export async function getConnection(): Promise<amqp.Channel | null> {
    if (!channel) await createConnection();
    return channel;
}