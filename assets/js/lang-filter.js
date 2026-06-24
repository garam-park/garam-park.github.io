// 홈 글 목록의 한/영 언어 필터.
// 각 글의 data-lang 속성을 기준으로 페이지 이동 없이 즉시 표시/숨김 한다.
// 선택값은 localStorage에 저장해 페이지네이션 이동에도 유지하고,
// 첫 진입 시에는 브라우저 언어로 기본 필터를 정한다(지원 외/감지 실패 시 전체).
(function () {
  var KEY = 'preferredLang';
  var nav = document.querySelector('.lang-filter');
  if (!nav) return;

  var buttons = nav.querySelectorAll('.lang-filter-btn');
  var posts = document.querySelectorAll('#post-list .post');
  var empty = document.querySelector('.lang-filter-empty');

  function isValid(v) { return v === 'all' || v === 'ko' || v === 'en'; }

  function detectDefault() {
    var saved = null;
    try { saved = localStorage.getItem(KEY); } catch (e) {}
    if (isValid(saved)) return saved;            // 사용자가 고른 값 우선

    var lang = (navigator.language || navigator.userLanguage || '').toLowerCase();
    if (lang.indexOf('ko') === 0) return 'ko';
    if (lang.indexOf('en') === 0) return 'en';
    return 'all';                                 // 지원 외 언어/감지 실패 → 전체
  }

  function apply(filter) {
    var shown = 0;
    posts.forEach(function (p) {
      var match = filter === 'all' || p.getAttribute('data-lang') === filter;
      p.hidden = !match;
      if (match) shown++;
    });
    buttons.forEach(function (b) {
      b.classList.toggle('is-active', b.getAttribute('data-filter') === filter);
    });
    if (empty) empty.hidden = shown !== 0;
    try { localStorage.setItem(KEY, filter); } catch (e) {}
  }

  buttons.forEach(function (b) {
    b.addEventListener('click', function () { apply(b.getAttribute('data-filter')); });
  });

  apply(detectDefault());
})();
