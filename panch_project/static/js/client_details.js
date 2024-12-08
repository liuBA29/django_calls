document.addEventListener('DOMContentLoaded', function() {
    // Находим все изображения клиентов
    const clientImages = document.querySelectorAll('img');

    // Создаем модальное окно
    const modal = document.createElement('div');
    modal.style.display = 'none';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    modal.style.zIndex = '1000';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
    modal.style.textAlign = 'center';
    modal.innerHTML = '<div style="position: relative; display: inline-block; max-width: 90%; max-height: 90%;">' +
                        '<span id="closeModal" style="position: absolute; top: 10px; right: 20px; font-size: 30px; color: white; cursor: pointer;">&times;</span>' +
                        '<img id="modalImage" style="max-width: 100%; max-height: 100%;" />' +
                     '</div>';
    document.body.appendChild(modal);

    // Открытие модального окна с изображением
    clientImages.forEach(img => {
        img.addEventListener('click', function() {
            const modalImage = document.getElementById('modalImage');
            modalImage.src = img.src;
            modal.style.display = 'flex';  // Показываем модальное окно
        });
    });

    // Закрытие модального окна при клике на крестик
    const closeModal = document.getElementById('closeModal');
    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';  // Скрыть модальное окно
    });

    // Закрытие модального окна при клике в любом месте на фоне
    modal.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';  // Скрыть модальное окно
        }
    });
});
