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
            const messageDiv = document.createElement('div');
            messageDiv.style.display = 'flex';
            messageDiv.style.alignItems = 'center';
            messageDiv.style.marginBottom = '10px';

            // Если у записи есть изображение, добавляем его
            if (record.client_image) {
                const imageElement = document.createElement('img');
                imageElement.src = record.client_image;
                imageElement.alt = 'Client Image';
                imageElement.style.width = '50px';
                imageElement.style.height = '50px';
                imageElement.style.borderRadius = '50%';
                imageElement.style.marginRight = '10px';
                messageDiv.appendChild(imageElement);
            }

            const textElement = document.createElement('span');
            textElement.innerText = `Звонит клиент: ${record.client_name}`;
            messageDiv.appendChild(textElement);

            dynamicContentDiv.appendChild(messageDiv);
        });
    }
}

// Обновляем данные каждые 3 секунды
setInterval(fetchCallRecords, 2000);
fetchCallRecords(); // Первоначальный вызов
