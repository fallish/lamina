

function obj2table(obj) {
    html = '<table class="popup">';
    html += '<thead><tr><td>k</td><td>v</td></tr></thead>';
    html += '<tbody>';
    for (let k in obj) {
        v = obj[k];
        html += '<tr>'
        html += '<td>' + k + '</td>';
        html += '<td>' + v + '</td>';
        html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';

//    html = '<div>' + html + '</div>';
    return html;
}
