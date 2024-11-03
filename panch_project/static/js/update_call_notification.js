const updateUrl = "/calls/get_call_records/"; // Обновите этот URL на тот, который используется для получения звонков

setInterval(() => {
    fetch(updateUrl)
        .then(response => response.json())
        .then(data => {
            const { call_records } = data;
            if (call_records && call_records.length > 0) {
                // Предположим, что последние звонки - это последние в массиве
                const latestCall = call_records[call_records.length - 1];
                showCallNotification(latestCall.calling_number);
            }
        })
        .catch(error => console.error('Ошибка при получении данных:', error));
}, 3000); // Обновляем каждые 3 секунды

function showCallNotification(callingNumber) {
    const message = `Вам звонят с номера: ${callingNumber}`;
    alert(message); // Или вы можете использовать другой способ отображения сообщения
}
