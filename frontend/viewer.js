const outlineFile = 'outline.json';
const pdfFileUrl = 'https://raw.githubusercontent.com/jainnVartika/Adobe_hackathon/main/sample.pdf';

const adobeDCViewPromise = new Promise((resolve) => {
  document.addEventListener("adobe_dc_view_sdk.ready", function () {
    const adobeDCView = new AdobeDC.View({
      clientId: "ff4d034306fd41a5a2b2f1f094db6802",
      divId: "adobe-dc-view"
    });

    adobeDCView.previewFile({
      content: { location: { url: pdfFileUrl } },
      metaData: { fileName: "sample.pdf" }
    }, { embedMode: "SIZED_CONTAINER" });

    resolve(adobeDCView);
  });
});

fetch(outlineFile)
  .then(res => res.json())
  .then(data => {
    const outlineList = document.getElementById('outlineList');
    const searchInput = document.getElementById('searchBar');

    function renderList(filteredOutline) {
      outlineList.innerHTML = '';
      filteredOutline.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.level} - ${item.text}`;
        li.setAttribute('data-level', item.level);
        li.onclick = () => {
          adobeDCViewPromise.then(view => view.gotoLocation({ pageNumber: item.page }));
        };
        outlineList.appendChild(li);
      });
    }

    const fullList = [
  {
    level: 'TITLE',
    text: data.title || 'Untitled Document',
    page: 1,
    section_type: 'title'
  },
  ...data.outline
];
renderList(fullList);


    searchInput.addEventListener('input', () => {
      const keyword = searchInput.value.toLowerCase();
      const filtered = data.outline.filter(item =>
        item.text.toLowerCase().includes(keyword)
      );
      renderList(filtered);
    });
  });

/** 🔄 Theme Switching */
const themeBtn = document.querySelector(".theme-toggle");
const themeDropdown = document.querySelector(".theme-dropdown-content");

themeBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  themeDropdown.classList.toggle("show");
});

// Close dropdown if clicking outside
document.addEventListener("click", () => {
  themeDropdown.classList.remove("show");
});

// Theme setter
function setTheme(theme) {
  if (theme === 'dark') {
    document.body.classList.add('dark-mode');
    localStorage.setItem('theme', 'dark');
  } else {
    document.body.classList.remove('dark-mode');
    localStorage.setItem('theme', 'light');
  }
}

// Load saved theme
(function initializeTheme() {
  const savedTheme = localStorage.getItem('theme') || 'light';
  setTheme(savedTheme);
})();
