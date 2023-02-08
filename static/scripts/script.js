function showText(cardId) {
    var card = document.getElementById(cardId);
    var image = card.querySelector('#image-' + cardId.split('-')[1]);
    var text = card.querySelector('#text-' + cardId.split('-')[1]);
    image.classList.toggle("invisible");
    text.classList.toggle("invisible");
}