export default function handleNotifications(toast) {
    let messages = JSON.parse(localStorage.getItem('messages'))
    for (let messageIndex in messages) {    
      let message = JSON.parse(messages[messageIndex])
      console.log(message)    
      toast.add({severity: message.severity, summary: message.title, detail: message.body, life: 3000});
      delete messages[messageIndex]
    }
    localStorage.setItem('messages', JSON.stringify(messages));
}
