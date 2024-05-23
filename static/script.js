document.addEventListener('DOMContentLoaded', function() {
    const leftSidebar = document.getElementById('left-sidebar');
    const rightSidebar = document.getElementById('right-sidebar');
    const toggleLeftBtn = document.getElementById('toggle-left-btn');
    const toggleRightBtn = document.getElementById('toggle-right-btn');

    toggleLeftBtn.addEventListener('click', function() {
        leftSidebar.classList.toggle('collapsed');
    });

    toggleRightBtn.addEventListener('click', function() {
        rightSidebar.classList.toggle('collapsed');
    });

    // Hide sidebars by default on small screens
    if (window.innerWidth < 1000) {
        leftSidebar.classList.add('collapsed');
        rightSidebar.classList.add('collapsed');
    }
});
