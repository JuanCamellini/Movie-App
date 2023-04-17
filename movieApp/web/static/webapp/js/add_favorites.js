<script>
  favoriteLinks.forEach(link => {
    link.addEventListener('click', event => {
      // We prevent the default action of the link
      event.preventDefault();

      // We get the form to which the link belongs
      const form = event.target.parentElement;

      // We create a FormData object with the form data
      const formData = new FormData(form);

      // We add an entry to the FormData with the name of the view action
      formData.append('action', 'add_to_favorites');

      // We make a POST request with the form data
      fetch('{% url "movie_detail" movie.id %}', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (response.ok) {
          // If the response is successful, we show a confirmation message
          alert('Movie added to favorites');
        } else {
          // If the response is not successful, we show an error message
          alert('Error adding movie to favorites');
        }
      })
      .catch(error => {
        // If there is an error in the request, we show an error message
        alert('Error adding movie to favorites');
        console.error(error);
      });
    });
    });
</script>