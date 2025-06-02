document.addEventListener("DOMContentLoaded", function () {
  // rootId приходит из шаблона, объявлен в <script> на странице
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
