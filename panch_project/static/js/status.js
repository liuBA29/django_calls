// static/js/status.js
document.addEventListener('DOMContentLoaded', function () {
    setInterval(function() {
        // Отправляем запрос на сервер для получения статуса звонка
        fetch('/get-call-status/')
            .then(response => response.json())
            .then(data => {
                // Используем полученный статус звонка
                const asteriskStatus = document.querySelector('.asterisk-status');
                const callingInfo = document.querySelector('.calling-info');
                if (data.is_active_call) {
                    // Если есть активный звонок, отображаем это
                    asteriskStatus.classList.remove('failure');
                    asteriskStatus.classList.add('success');
                    if (data.calling_number){
                    callingInfo.textContent = 'Вам звонят!${data.calling_number}';
                    callingInfo.style.display = 'block';
                    }
                }

                else {
                    // Если нет активных звонков, отображаем это
                    asteriskStatus.classList.remove('success');
                    asteriskStatus.classList.add('failure');
                }
            })
            .catch(error => console.error('Error fetching call status:', error));
    }, 3000);  // обновление каждые 3 секунды
});


