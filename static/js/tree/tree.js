document.addEventListener("DOMContentLoaded", function () {
  // Инициализация основного дерева
  fetch(`/tree/data/${rootId}/`)
    .then(response => {
      if (!response.ok) throw new Error('Ошибка загрузки данных: ' + response.status);
      return response.json();
    })
    .then(data => {
      const chart_config = {
        chart: {
          container: "#tree-simple",
          node: {
            collapsable: true
          },
          animation: {
            nodeAnimation: "easeOutBounce",
            nodeSpeed: 700,
            connectorsAnimation: "bounce",
            connectorsSpeed: 700
          },
          callback: {
            onRender: function () {
              // Переключатели разворачивания узлов
              document.querySelectorAll(".collapse-switch").forEach(el => {
                if (!el.dataset.init) {
                  el.textContent = "+";
                  el.dataset.init = "true";
                  el.addEventListener("click", function () {
                    this.textContent = this.textContent === "+" ? "–" : "+";
                  });
                }
              });
            }
          }
        },
        nodeStructure: data
      };

      new Treant(chart_config);
    })
    .catch(error => {
      console.error('Ошибка при получении данных для дерева:', error);
    });
});
