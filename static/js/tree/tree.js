document.addEventListener("DOMContentLoaded", function () {
  fetch(`/tree/data/${rootId}/`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Ошибка загрузки данных: ' + response.status);
      }
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
              // Инициализация переключателей сворачивания узлов
              document.querySelectorAll(".collapse-switch").forEach(el => {
                if (!el.dataset.init) {
                  el.textContent = "+";
                  el.dataset.init = "true";
                  el.addEventListener("click", function () {
                    this.textContent = this.textContent === "+" ? "–" : "+";
                  });
                }
              });

              // Обработчик клика по узлам для линии жены
              document.querySelectorAll(".wife-line-toggle").forEach(button => {
                if (!button.dataset.listenerAdded) {
                  button.dataset.listenerAdded = "true";
                  button.addEventListener("click", function (e) {
                    e.stopPropagation();
                    const wifeId = this.dataset.wifeId;
                    if (!wifeId) return;

                    const containerId = `wife-tree-container-${wifeId}`;
                    let container = document.getElementById(containerId);

                    if (container) {
                      // Уже загружено — переключаем видимость
                      container.style.display = container.style.display === "none" ? "block" : "none";
                      return;
                    }

                    // Создаём контейнер для дерева жены
                    container = document.createElement("div");
                    container.id = containerId;
                    container.style.marginLeft = "20px";
                    this.insertAdjacentElement("afterend", container);

                    // Загружаем данные линии жены
                    fetch(`/tree/data/${wifeId}/`)
                      .then(resp => resp.json())
                      .then(wifeData => {
                        // Отрисовка дерева жены (упрощённо, можно расширить)
                        const wifeChartConfig = {
                          chart: {
                            container: `#${containerId}`,
                            node: {
                              collapsable: true
                            },
                            animation: {
                              nodeAnimation: "easeOutBounce",
                              nodeSpeed: 700,
                              connectorsAnimation: "bounce",
                              connectorsSpeed: 700
                            }
                          },
                          nodeStructure: wifeData
                        };
                        new Treant(wifeChartConfig);
                      })
                      .catch(() => {
                        container.textContent = "Ошибка загрузки родословной жены";
                      });
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
