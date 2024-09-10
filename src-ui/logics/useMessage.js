import {
    useMessageLogsStatus,
} from "@store";

import { useStdoutToPython } from "@logics/useStdoutToPython";

export const useMessage = () => {
    const { currentMessageLogsStatus, addMessageLogsStatus, updateMessageLogsStatus } = useMessageLogsStatus();
    const { asyncStdoutToPython } = useStdoutToPython();

    const sendMessage = (message) => {
        const uuid = crypto.randomUUID();
        const send_message_object = {
            id: uuid,
            message: message,
        };
        asyncStdoutToPython("/controller/callback_messagebox_send", send_message_object);

        addMessageLogsStatus({
            id: uuid,
            category: "sent",
            status: "pending",
            created_at: generateTimeData(),
            messages: {
                original: message,
                translated: [],
            },
        });
    };

    const updateSentMessageLogById = (payload) => {
        updateMessageLogsStatus(updateItemById(data.id, payload.translation));
    };
    const addSentMessageLog = (payload) => {
        const message_object = generateMessageObject(payload, "sent");
        addMessageLogsStatus(message_object);
    };
    const addReceivedMessageLog = (payload) => {
        const message_object = generateMessageObject(payload, "received");
        addMessageLogsStatus(message_object);
    };

    return {
        currentMessageLogsStatus,
        sendMessage,
        updateSentMessageLogById,
        addSentMessageLog,
        addReceivedMessageLog,
    };
};

const generateTimeData = () => {
    const data = new Date().toLocaleTimeString(
        "ja-JP",
        {hour12: false, hour: "2-digit", minute: "2-digit"},
    );
    return data;
};

const generateMessageObject = (data, category) => {
    return {
        id: crypto.randomUUID(),
        created_at: generateTimeData(),
        category: category,
        status: "ok",
        messages: {
            original: data.message,
            translated: data.translation,
        },
    };
};


const updateItemById = (id, translated_data) => (prev_items) => {
    return prev_items.map(item => {
        if (item.id === id) {
            item.status = "ok";
            item.messages.translated = translated_data;
        }
        return item;
    });
};