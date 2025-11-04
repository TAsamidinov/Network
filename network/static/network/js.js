document.addEventListener('DOMContentLoaded', () => {

  document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', async () => {
      const postId = button.dataset.postId;
      const likeCount = document.querySelector(`#like-count-${postId}`);
  
      try {
        const response = await fetch(`/like/${postId}/`, {
          method: 'POST',
          headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        if (!response.ok) throw new Error('Network error');
  
        const result = await response.json();
  
        likeCount.textContent = result.likes;
  
        // Change button text and active state instantly
        if (result.liked) {
          
          button.innerHTML = `Unlike: <span id="like-count-${postId}">${result.likes}</span>`;
          button.classList.add('active');
        } else {
          button.innerHTML = `Like: <span id="like-count-${postId}">${result.likes}</span>`;
          button.classList.remove('active');
        }
  
      } catch (err) {
        console.error('Error:', err);
      }
    });
  });

  document.querySelectorAll('.edit-btn').forEach(button => {
    button.onclick = function () {
      const editButton = this; 
      editButton.disabled = true; 

      const postId = this.dataset.postId;
      const contentDiv = document.querySelector(`#content-${postId}`);
      if (!contentDiv) return;

      const originalHTML = contentDiv.innerHTML;
      const originalText = contentDiv.innerText.trim();


      const textarea = document.createElement('textarea');
      textarea.className = 'form-control';
      textarea.value = originalText;
      textarea.style.width = '100%';
      textarea.style.resize = 'none'; 
      textarea.style.overflow = 'hidden';
      textarea.style.minHeight = contentDiv.scrollHeight + 20 + 'px'; 
      textarea.style.height = contentDiv.scrollHeight + 20 + 'px';

      textarea.addEventListener('input', () => {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
      });

      const actions = document.createElement('div');
      actions.className = 'd-flex justify-content-end align-items-center';

      const saveButton = document.createElement('button');
      saveButton.className = 'btn btn-success';
      saveButton.textContent = 'Save';

      const cancelButton = document.createElement('button');
      cancelButton.className = 'btn btn-secondary';
      cancelButton.textContent = 'Cancel';

      const status = document.createElement('span');
      status.className = 'ms-auto small text-muted';

      actions.append(status, saveButton, cancelButton);
      actions.style.gap = '12px';
      actions.style.marginTop = '0.5rem';

      contentDiv.innerHTML = '';
      contentDiv.append(textarea, actions);
      textarea.focus();

      cancelButton.onclick = () => (
        contentDiv.innerHTML = originalHTML,
        editButton.disabled = false
      );

      saveButton.onclick = async () => {
        const newContent = textarea.value.trim();
        if (!newContent) { 
          status.textContent = 'Content is empty'; 

          return; 
        }

        saveButton.disabled = true;
        cancelButton.disabled = true;
        textarea.disabled = true;
        status.textContent = 'Saving…';

        try {
          const response = await fetch(`/edit/${postId}/`, {
            method: 'PUT',
            headers: {
              'X-CSRFToken': getCookie('csrftoken'),
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: newContent })
          });

          if (!response.ok) throw new Error(await response.text());
          const result = await response.json();

          const p = document.createElement('p');
          p.textContent = result.content;
          contentDiv.innerHTML = '';
          contentDiv.appendChild(p);
          editButton.disabled = false;
        } catch (err) {
          status.textContent = 'Error saving. Try again.';
          saveButton.disabled = false;
          cancelButton.disabled = false;
          textarea.disabled = false;
          console.error(err);
        }

      };
    };
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
      c = c.trim();
      if (c.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(c.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}