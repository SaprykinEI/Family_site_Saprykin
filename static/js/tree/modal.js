document.addEventListener("DOMContentLoaded", function () {
  // Создаем модальное окно, если его нет
  if (!document.getElementById("spouse-tree-modal")) {
    const modal = document.createElement("div");
    modal.id = "spouse-tree-modal";
    modal.innerHTML = `
      <div class="modal-content">
        <button class="close-btn" title="Закрыть окно">×</button>
        <div id="spouse-tree-container" style="min-height: 400px;">
          <!-- Здесь будет содержимое модального окна -->
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    // Обработчик закрытия по кнопке
    modal.querySelector(".close-btn").addEventListener("click", () => {
      modal.style.display = "none";
      // Очищаем содержимое, чтобы дерево удалялось при закрытии
      document.getElementById("spouse-tree-container").innerHTML = "";
    });

    // Обработчик закрытия при клике вне содержимого
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.style.display = "none";
        document.getElementById("spouse-tree-container").innerHTML = "";
      }
    });
  }

  // Делегирование: ловим клики по элементам с классом .spouse-wrapper
  document.addEventListener("click", function (e) {
    const spouseEl = e.target.closest(".spouse-wrapper");
    if (spouseEl) {
      e.stopPropagation();
      const modal = document.getElementById("spouse-tree-modal");
      modal.style.display = "block";

      const container = document.getElementById("spouse-tree-container");
      container.innerHTML = "<p>Загрузка дерева супруги...</p>";

      const spouseId = spouseEl.dataset.spouseId;

      // Запрос данных для дерева супруги с сервера
      fetch(`/tree/data/spouse/${spouseId}/`)
        .then(response => {
          if (!response.ok) throw new Error('Ошибка загрузки данных: ' + response.status);
          return response.json();
        })
        .then(data => {
          container.innerHTML = ""; // очищаем контейнер

          const config = {
            chart: {
              container: "#spouse-tree-container",
              node: { collapsable: true },
              animation: {
                nodeAnimation: "easeOutBounce",
                nodeSpeed: 700,
                connectorsAnimation: "bounce",
                connectorsSpeed: 700
              }
            },
            nodeStructure: data
          };

          new Treant(config);
        })
        .catch(error => {
          container.innerHTML = `<p style="color:red;">Ошибка: ${error.message}</p>`;
        });
    }
  });
});


function transformAncestorsData(data) {
  // Визуализация ожидает поле children
  if (data.parents) {
    data.children = data.parents;
    delete data.parents;
  }
  // Рекурсивно применяем к детям
  if (data.children) {
    data.children.forEach(transformAncestorsData);
  }
  return data;
}
