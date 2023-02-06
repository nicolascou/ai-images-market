const header = document.querySelector('header');
const body = document.querySelector('body');
const mobileNav = document.getElementById('mobile-nav_id')

const handleScroll = () => {
    if (document.documentElement.scrollTop > 1) {
        header.classList.add('header-scrolled');
    } else {
        header.classList.remove('header-scrolled');
    }
}

window.addEventListener('scroll', () => {
    handleScroll();
})

const toggleMobileNav = () => {
    mobileNav.classList.toggle('mobile-nav-translate');
    header.classList.toggle('header-scrolled');
    body.classList.toggle('overflow-hidden');
}

window.addEventListener('resize', () => {
    if (window.innerWidth > 900 && mobileNav.classList.contains('mobile-nav-translate')) {
        toggleMobileNav();
    }
})

// Focus when pressed in search header button
const search = document.getElementById("header-to-search");

if (search) {
    search.addEventListener("click", () => {
        document.querySelector("#left-bar-search").focus();
    });
}

  