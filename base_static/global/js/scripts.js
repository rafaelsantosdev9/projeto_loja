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


(function () {
    select_variacao = document.getElementById('select-variacoes');
    variation_preco = document.getElementById('variation-preco');
    variation_preco_promocional = document.getElementById('variation-preco-promocional');

    if (!select_variacao) {
        return;
    }

    if (!variation_preco) {
        return;
    }

    select_variacao.addEventListener('change', function () {
        preco = this.options[this.selectedIndex].getAttribute('data-preco');
        preco_promocional = this.options[this.selectedIndex].getAttribute('data-preco-promocional');


        if (preco && variation_preco) {
            variation_preco.innerHTML = preco;
        }
        
        if (variation_preco_promocional && preco_promocional) {
            variation_preco_promocional.innerHTML = preco_promocional;
        } else {
            variation_preco_promocional.innerHTML = preco;
            variation_preco.innerHTML = ''
        }

    })
})();
document.getElementById('form-add-to-cart').addEventListener('submit', function (event) {
    const selectVariacao = document.getElementById('select-variacoes');
    if (selectVariacao && !selectVariacao.value) {
        event.preventDefault();
        alert('Por favor, selecione uma variação do produto.');
    }
});
const selectVariacao = document.getElementById('select-variacoes');
if (!selectVariacao || selectVariacao.options.length === 0) {
    // Produto sem variações; desabilitar validação de variação
    document.getElementById('form-add-to-cart').submit();
}

// TROCA DE IMAGEM DO DETALHE.HTML
document.addEventListener('DOMContentLoaded', function () {
    const selectVariacoes = document.getElementById('select-variacoes');
    const imgElement = document.getElementById('produto-img');

    selectVariacoes.addEventListener('change', function () {
      const selectedOption = this.options[this.selectedIndex];
      const newImageUrl = selectedOption.getAttribute('data-img');

      if (newImageUrl && imgElement) {
        imgElement.src = newImageUrl;
      }

      // Também pode atualizar preços se quiser
      const preco = selectedOption.getAttribute('data-preco');
      const precoPromocional = selectedOption.getAttribute('data-preco-promocional');

      const precoEl = document.getElementById('variation-preco');
      const precoPromoEl = document.getElementById('variation-preco-promocional');

      if (precoPromoEl && precoPromocional && precoPromocional.trim() !== '') {
        precoPromoEl.textContent = precoPromocional;
        precoEl.textContent = preco;
        precoPromoEl.style.display = 'inline';
        precoEl.classList.add('text-decoration-line-through');
      } else {
        precoEl.textContent = preco;
        if (precoPromoEl) precoPromoEl.style.display = 'none';
        precoEl.classList.remove('text-decoration-line-through');
      }
    });
  });
  document.addEventListener('DOMContentLoaded', function () {
    const carrinhoImagens = document.querySelectorAll('td img.img-thumbnail');

    carrinhoImagens.forEach(function (img) {
        img.onerror = function () {
            this.src = '/static/img/sem-imagem.png'; // Caminho padrão para imagem de fallback
        };
    });
});