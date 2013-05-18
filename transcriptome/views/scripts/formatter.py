def clustal_to_html(clustal_content, seqtype):
    """
    seqtype: n or a
    """
    match_table = {'*': '<span class="ast">*</span>',
                   '.': '<span class="dot">.</span>',
                   ':': '<span class="col">:</span>',
                   '-': '<span class="gap">-</span>'}

    html = []
    lines = clustal_content.split('\n')

    html.append('<div class="alignment">')
    html.append('<span class="title">' + lines.pop(0) + '</span></br>')

    align_base_count = 0
    align_line_count = 0

    for line in lines:
        if line == '':
            html.append('</br>')

        elif line[0] == ' ':
            for c in line[1:]:
                if c == ' ':
                    html.append('&nbsp')
                else:
                    html.append(match_table.get(c))

            html.append('&nbsp<span class="count">' + str(align_base_count / align_line_count) + '</span></br>')
            align_line_count = 0

        else:
            data = line.split(' ')

            html.append('<span class="n' + str(align_line_count) + '">' + data[0] + '</span>')

            for c in data[1:-1]:
                html.append('&nbsp')

            for c in data[-1]:
                if c == '-':
                    html.append(match_table.get(c))
                else:
                    html.append('<span class="' + seqtype + c + '">' + c + '</span>')

            html.append('</br>')

            align_line_count += 1
            align_base_count += len(data[-1])

    html.append('</div>')

    return ''.join(html)
