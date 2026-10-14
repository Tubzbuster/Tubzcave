// Shared on every page.

// ---------- 1. Image path fallbacks ----------
// <img class="fb" data-srcs="images/a.gif|a.gif" data-icon="px-film" data-missing="text"> tries each path in order.
// If none load: shows the pixel icon named in data-icon, or a dashed box with data-missing text.
function runFallbacks(root) {
  var imgs = (root || document).querySelectorAll("img.fb");
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
}
runFallbacks(document);

// ---------- 2. Floating music button (plays music.mp3 from the same folder as the pages) ----------
(function () {
  var btn = document.getElementById("musicBtn");
  if (!btn) return;
  var KEY = "anya-music";
  var audio = new Audio("music.mp3");
  audio.loop = true;
  audio.preload = "none"; // do not download music.mp3 until someone presses play

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
  var lastSave = 0; // save the position every couple of seconds, not 4x a second
  audio.addEventListener("timeupdate", function () {
    var n = Date.now();
    if (n - lastSave > 2000) { lastSave = n; save(); }
  });
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

// ---------- 2b. Pause animations that are scrolled out of view (saves CPU) ----------
(function () {
  if (!("IntersectionObserver" in window)) { window.watchAnimations = function () {}; return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { en.target.classList.toggle("anim-off", !en.isIntersecting); });
  });
  window.watchAnimations = function () {
    io.disconnect();
    Array.prototype.forEach.call(document.querySelectorAll("[data-anim]"), function (el) { io.observe(el); });
  };
  window.watchAnimations();
})();

// ---------- 3. Page changes without a reload (so the music keeps playing) ----------
// Clicking a link to another page of this site fetches it and swaps the content in,
// instead of loading a brand new page. The music button and its audio stay untouched.
// If anything goes wrong it just does a normal page load.
(function () {
  if (!window.fetch || !window.DOMParser || !window.AbortController || !history.pushState) return;
  var here = location.pathname;

  function swap(doc) {
    if (window.pageAbort) { window.pageAbort.abort(); window.pageAbort = null; }
    document.title = doc.title;
    var keep = document.getElementById("musicBtn");
    Array.prototype.slice.call(document.body.children).forEach(function (n) { if (n !== keep) n.remove(); });
    var scripts = [];
    Array.prototype.slice.call(doc.body.children).forEach(function (n) {
      if (n.id === "musicBtn") return;
      if (n.tagName === "SCRIPT") { scripts.push(n); return; }
      document.body.appendChild(document.importNode(n, true));
    });
    runFallbacks(document.body);
    if (window.watchAnimations) window.watchAnimations();
    scripts.forEach(function (sc) {
      if (sc.src) return; // site.js is already running
      var x = document.createElement("script");
      x.text = sc.textContent;
      document.body.appendChild(x);
    });
    window.scrollTo(0, 0);
  }

  function go(url, push) {
    fetch(url, { credentials: "same-origin" })
      .then(function (r) { if (!r.ok) throw new Error("bad response"); return r.text(); })
      .then(function (html) {
        swap(new DOMParser().parseFromString(html, "text/html"));
        if (push) history.pushState({}, "", url);
        here = location.pathname;
      })
      .catch(function () { location.href = url; });
  }

  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a || a.target || a.hasAttribute("download") || a.hasAttribute("data-open")) return;
    if ((a.getAttribute("href") || "").charAt(0) === "#") return;
    var u = new URL(a.href, location.href);
    if (u.origin !== location.origin || !/(\.html|\/)$/.test(u.pathname)) return;
    e.preventDefault();
    go(u.href, true);
  });

  window.addEventListener("popstate", function () {
    if (location.pathname !== here) go(location.href, false);
  });
})();
