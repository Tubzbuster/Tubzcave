// Shared on every page.

// ---------- 1. Image path fallbacks ----------
// <img class="fb" data-srcs="images/a.gif|a.gif" data-icon="px-film" data-missing="text"> tries each path in order.
// If none load: shows the pixel icon named in data-icon, or a dashed box with data-missing text.
(function () {
  var imgs = document.querySelectorAll("img.fb");
  Array.prototype.forEach.call(imgs, function (img) {
    var list = (img.getAttribute("data-srcs") || "").split("|").filter(Boolean);
    var i = 0;
    function giveUp() {
      img.removeEventListener("error", next);
      var icon = img.getAttribute("data-icon");
      var repl;
      if (icon) {
        repl = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        repl.setAttribute("viewBox", "0 0 24 24");
        repl.setAttribute("class", (img.className.replace("fb", "") + " fb-icon").trim());
        repl.setAttribute("aria-hidden", "true");
        var use = document.createElementNS("http://www.w3.org/2000/svg", "use");
        use.setAttributeNS("http://www.w3.org/1999/xlink", "href", "#" + icon);
        use.setAttribute("href", "#" + icon);
        repl.appendChild(use);
      } else {
        repl = document.createElement("div");
        repl.className = "fb-missing";
        repl.textContent = img.getAttribute("data-missing") || "image not found";
      }
      img.parentNode.replaceChild(repl, img);
    }
    function next() {
      if (i < list.length) { img.src = list[i++]; } else { giveUp(); }
    }
    img.addEventListener("error", next);
    next();
  });
})();

// ---------- 2. Floating music button (plays music.mp3 from the same folder as the pages) ----------
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
