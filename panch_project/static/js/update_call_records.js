
async function fetchCallRecords() {
    try {
        const response = await fetch('/calls/get_call_records/');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        updateDynamicContent(data.call_records);
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}

function updateDynamicContent(callRecords) {
    const dynamicContentDiv = document.getElementById('dynamic-content');
    dynamicContentDiv.innerHTML = ''; // Очищаем текущее содержимое

    if (callRecords.length === 0) {
        dynamicContentDiv.innerHTML = 'Нет входящих звонков.';
    } else {
        callRecords.forEach(record => {
            const message = document.createElement('div');
            message.innerText = `Вам звонят с номера: ${record.calling_number}`;
            dynamicContentDiv.appendChild(message);
        });
    }
}

// Обновляем данные каждые 3 секунды
setInterval(fetchCallRecords, 2000);
fetchCallRecords(); // Первоначальный вызов
