from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def criar_nota(self, nome_nota, obj, valtot, desconto):
        # Criar um objeto Story para armazenar o conteúdo do PDF
        doc = SimpleDocTemplate(nome_nota, pagesize=letter)

        # Estilos de texto
        styles = getSampleStyleSheet()
        titulo_style = styles["Heading1"]
        titulo_style.leftIndent = -50
        titulo_style.fontSize = 24
        titulo_style.fontname = 'Calibri'

        subtitulo_style = styles['Normal']
        subtitulo_style.fontSize = 10
        subtitulo_style.fontname = 'Calibri'

        paragrafo_style = styles["Normal"]
        paragrafo_style.leftIndent = -50
        paragrafo_style.rightIndent = -50
        # Conteúdo da nota fiscal
        story = []

        story.append(Paragraph("AUTO MECÂNICA AUTOMEC", titulo_style))
        story.append(Paragraph("RUA VIDEIRA, 555 – PARQUE DOS LAGOS, JACAREÍ – SP" + "&nbsp;"*44 + "(12)98811-1111", subtitulo_style))
        story.append(Paragraph('_'*100, paragrafo_style))

        # Informações do nota
        story.append(Spacer(1, 5))
        story.append(Paragraph(f"Ordem de Serviço: {int(obj.ordem):010d}" + "&nbsp;"*121 + f"Data: {obj.data}", paragrafo_style))
        story.append(Paragraph('_'*100, paragrafo_style))

        # Informações do cliente
        story.append(Spacer(1, 5))
        story.append(Paragraph(f"Cliente: {obj.ncliente}", paragrafo_style))
        story.append(Paragraph(f"Telefone: {obj.telefone}", paragrafo_style))
        story.append(Paragraph('_'*100, paragrafo_style))

        story.append(Spacer(1, 5))
        story.append(Paragraph(f"PLACA DO VEÍCULO: {obj.placa}" + "&nbsp;"*20 + f"MARCA: {obj.marca}" + "&nbsp;"*20 + f"MODELO: {obj.modelo}", paragrafo_style))
        story.append(Spacer(1, 5))
        story.append(Paragraph(f"COR DO VEÍCULO: {obj.cor}" + "&nbsp;"*20 + f"ANO: {obj.ano}" + "&nbsp;"*20 + f"Quilometragem: {obj.kmatual}", paragrafo_style))
        story.append(Paragraph('_'*100, paragrafo_style))

        #Observações
        story.append(Spacer(1, 5))
        story.append(Paragraph(f"Observações Gerais: {obj.observacoes}", paragrafo_style))
        story.append(Paragraph('_'*100, paragrafo_style))

        # Tabela de itens da compra
        story.append(Spacer(1, 5))
        table_data = [['Descrição da Peça'+' '*108, '   Valor', 'Quantia', '   Valor Total']]
        for item in obj.pecas:
            table_data.append([item[0][:100], f'{item[1]:.2f}'[:7], str(item[2])[:5], f'{item[3]:.2f}'[:9]])

        t = Table(table_data)
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('FONTSIZE', (0, 0), (-1, -1), 10),]))

        story.append(t)
        story.append(Paragraph('_'*100, paragrafo_style))

        # Total das Peças e Mão de Obra
        table_data = [[' '*180, '              ']]
        table_data.append(['Total das Peças:', f'{valtot:.2f}'[:9]])
        table_data.append(['Mão de Obra:', f'{obj.maodeobra:.2f}'[:9]])

        t = Table(table_data)
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('FONTSIZE', (0, 0), (-1, -1), 10)]))

        story.append(t)
        story.append(Paragraph('_'*100, paragrafo_style))

        # Totais
        table_data = [[' '*140, '                 ']]
        table_data.append(['VALOR PEÇAS:', f'{valtot:.2f}'[:12]])
        table_data.append(['VALOR SERVIÇOS:', f'{obj.maodeobra:.2f}'[:12]])
        table_data.append(['DESCONTO:', f'{desconto}%'[:12]])
        table_data.append(['VALOR TOTAL:', f'{((valtot + obj.maodeobra)*(1-(desconto/100))):.2f}'[:12]])

        t = Table(table_data)
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('FONTSIZE', (0, 0), (-1, -1), 12)]))

        story.append(t)
        story.append(Paragraph('_'*100, paragrafo_style))

        # Construir o PDF
        doc.topMargin = 20
        doc.build(story)