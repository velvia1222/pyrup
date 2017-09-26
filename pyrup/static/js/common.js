function confirmRemove() {
	if (confirm("一度削除すると元に戻せません。削除しますか？")) {
		return true;
	} else {
		return false;
	}
}
function moveSiteList() {
	location.href = "/site/list";
}
function moveSiteAdd() {
	location.href = "/site/register?mode=add";
}
function moveSiteEdit(site_id) {
	location.href = "/site/register?mode=edit&site_id=" + site_id;
}
function movePageList(site_id) {
	location.href = "/page/list?site_id=" + site_id;
}
function movePageAdd(site_id) {
	location.href = "/page/register?mode=add&site_id=" + site_id;
}
function movePageEdit(page_id) {
	location.href = "/page/register?mode=edit&page_id=" + page_id;
}
function moveContentList(page_id) {
	location.href = "/content/list?page_id=" + page_id;
}
function moveContentAdd(page_id) {
	location.href = "/content/register?mode=add&page_id=" + page_id;
}
function moveContentEdit(content_id) {
	location.href = "/content/register?mode=edit&content_id=" + content_id;
}
