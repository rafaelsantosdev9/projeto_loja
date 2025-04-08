document.addEventListener('DOMContentLoaded', function () {
    const botao = document.getElementById('botao-teste');

    if (botao) {
        botao.addEventListener('click', function () {
            alert("JavaScript funcionando! 🎉");
        });
    }
});


function revealOnScroll() {
    const cards = document.querySelectorAll('.animated-card');
    const triggerBottom = window.innerHeight * 0.9;

    cards.forEach(card => {
        const cardTop = card.getBoundingClientRect().top;

        if (cardTop < triggerBottom) {
            card.classList.add('reveal');
        }
    });
}

document.addEventListener('DOMContentLoaded', revealOnScroll);
window.addEventListener('scroll', revealOnScroll);


