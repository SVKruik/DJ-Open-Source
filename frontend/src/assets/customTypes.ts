// JavaScript Types
export enum ObjectTypes {
    bigint = "bigint",
    boolean = "boolean",
    function = "function",
    number = "number",
    object = "object",
    string = "string",
    symbol = "symbol",
    undefined = "undefined"
}

// Date Formatter
export type DateFormat = {
    "date": string,
    "time": string,
    "today": Date
}

// Prompt/Informational Message Types
export enum PromptTypes {
    info = "info",
    success = "success",
    warning = "warning",
    danger = "danger"
}