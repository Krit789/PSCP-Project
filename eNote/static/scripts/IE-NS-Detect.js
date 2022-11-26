var agent = navigator.userAgent;

function isIE() {
  return navigator.userAgent.match(/(MSIE|Trident)/);
}

function isNetscape() {
  var web_user_agent = window.navigator.userAgent
  if ((web_user_agent.substring(0, 9) == "Mozilla/4") && !web_user_agent.match(/(MSIE|Trident)/) || web_user_agent.match(/(Netscape)/)) {
    return true;
  } else {
    return false
  }
}
//function to show alert if it's IE or Netscape
function ShowUnsupportedAlert() {
  if (isIE()) {
    alert("Microsoft Internet Explorer is unsupported. Page may not display correctly, please consider upgrading to a newer browser.\n\nUser Agent:\n" + agent);
  } else if (isNetscape()) {
    alert("Netscape Navigator is unsupported. Page may not display correctly, please consider upgrading to a newer browser.\n\nUser Agent:\n" + agent);
  }
}
// alert("Netscape Navigator ("+ agent + ") is unsupported. Page may not display correctly, please consider upgrading to a newer browser.");