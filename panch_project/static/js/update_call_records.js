

    function updateContent() {
            fetch('/api/data/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('dynamic-content').innerHTML = data.new_content;
            })
            .catch(error => console.log('Ошибка:', error));
        }

        // Обновление каждые 13 секунд (300000 миллисекунд)
        setInterval(updateContent, 13000);
        updateContent(); // Обновить сразу после загрузки страницы
