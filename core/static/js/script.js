$(document).ready(function() {
    // Captura el botón de menú
    var menuToggle = $('#dropdownMenuButton');
    
    // Captura el menú desplegable
    var menuShow = $('.dropdown-menu');

    // Escucha el evento de clic en el botón de menú
    menuToggle.click(function() {
        // Muestra u oculta el menú desplegable
        menuShow.toggleClass('show');
    });
});