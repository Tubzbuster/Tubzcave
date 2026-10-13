// Shared on every page: floating music button (plays music.mp3 from the same folder as the HTML files)
(function () {
  var btn = document.getElementById("musicBtn");
  if (!btn) return;
  var KEY = "anya-music";
  var audio = new Audio("music.mp3");
  audio.loop = true;

  var state = { t: 0, p: false };
  try { state = JSON.parse(sessionStorage.getItem(KEY)) || state; } catch (e) {}
  var wantPlay = !!state.p;

  function save() {
    try { sessionStorage.setItem(KEY, JSON.stringify({ t: audio.currentTime, p: wantPlay })); } catch (e) {}
  }
  function sync() {
    var playing = !audio.paused;
    btn.classList.toggle("playing", playing);
    btn.setAttribute("aria-label", playing ? "Pause music" : "Play music");
  }
  audio.addEventListener("play", sync);
  audio.addEventListener("pause", sync);
  audio.addEventListener("timeupdate", save);
  window.addEventListener("pagehide", save);

  // Best-effort resume after changing pages (browsers may block this until you click once)
  audio.addEventListener("loadedmetadata", function () { audio.currentTime = state.t || 0; }, { once: true });
  if (wantPlay) { audio.play().catch(function () {}); }

  // Other parts of the page (like the video popup) can ask the music to pause
  window.addEventListener("anya:pause-music", function () {
    if (!audio.paused) { wantPlay = false; audio.pause(); save(); }
  });

  btn.addEventListener("click", function () {
    if (audio.paused) {
      wantPlay = true;
      audio.play().catch(function () {
        wantPlay = false;
        alert("Couldn't play music.mp3. Check that it's in the same folder as index.html.");
      });
    } else {
      wantPlay = false;
      audio.pause();
    }
    save();
  });
})();
