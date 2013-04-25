def clustal_to_html(clustal_content):
    html = []
    lines = clustal_content.split('\n')

    html.append('<span class="pairwise-alignment">' + lines.pop(0) + '</span></br>')

    align_base_count = 0
    align_line_count = 0

    for line in lines:
        if line == '':
            html.append('</br>')

        elif line[0] == ' ':
            html.append(line.replace(' ', '&nbsp') +
                        '&nbsp' +
                        '<span class="count">' + str(align_base_count / align_line_count) + '</span>' +
                        '</br>')
            align_line_count = 0

        else:
            data = line.split(' ')

            html.append('<span class="query-name">' + data[0] + '</span><br>')

            for c in data[1:-1]:
                html.append('&nbsp')

            for c in data[-1]:
                html.append('<span class="' + c + '">' + c + '</span>')

            html.append('</br>')

            align_line_count += 1
            align_base_count += len(data[-1])

    return ''.join(html)
