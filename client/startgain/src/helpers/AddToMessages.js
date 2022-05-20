export default function addToMessages(message) {
    let messages = JSON.parse(localStorage.getItem('messages'));
    if (!messages) {
        messages = {}
    }
    messages = {...messages, [Object.keys(messages).length]:JSON.stringify(message)}    
    localStorage.setItem('messages',  JSON.stringify(messages))
}