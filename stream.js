// Yeh code file ko Telegram se Chrome mein stream karega
export async function streamFile(msgId, CHANNEL_USERNAME) {
    // Hum Telegram ke Web Server ka use karke Chrome ko bypass link denge
    const directUrl = `https://t.me/s/${CHANNEL_USERNAME}/${msgId}`;
    const response = await fetch(directUrl);
    const html = await response.text();
    
    // Yahan hum internal download link extract karte hain
    return new Response(null, {
        status: 302,
        headers: {
            "Location": `https://t.me/${CHANNEL_USERNAME}/${msgId}?download=1`,
            "Content-Disposition": "attachment; filename=movie.mkv"
        }
    });
}
