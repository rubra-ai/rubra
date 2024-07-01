module.exports = function (context, options) {
  return {
    name: 'datatables-plugin',
    injectHtmlTags() {
      return {
        postBodyTags: [
          {
            tagName: 'script',
            innerHTML: `
              document.addEventListener('DOMContentLoaded', function() {
                if (typeof jQuery !== 'undefined' && typeof jQuery.fn.DataTable !== 'undefined') {
                  jQuery('#benchmarkTable').DataTable({
                    paging: false,
                    searching: false,
                    info: false
                  });
                }
              });
            `,
          },
        ],
      };
    },
  };
};