document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('searchInput').addEventListener('keyup', filterVideos);
        });
    
        function filterVideos() {
            var input, filter, videoList, videos, title, i, txtValue;
            input = document.getElementById('searchInput');
            filter = input.value.toLowerCase();
            videoList = document.getElementById("videoList");
            
            if (!videoList) {
                console.error('videoList element nao encontrado');
                return;
            }
    
            videos = videoList.getElementsByClassName('video-container');
            
            // Para cada video
            for (i = 0; i < videos.length; i++) {
                // Pegue o titulo do video que reside dentro da tag h3
                title = videos[i].getElementsByTagName("h3")[0];

                // O valor do texto pode ambo ser esses dois valores, a escolha depende da compatibilidade do browser.
                txtValue = title.textContent || title.innerText;

                // Se o nosso filtro é SUBSTRING do TÍTULO DO VÍDEO, mostra o vídeo.
                if (txtValue.toLowerCase().indexOf(filter) > -1) {
                    videos[i].style.display = "";
                } else {
                    videos[i].style.display = "none";
                }
            }
        }