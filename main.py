import cv2
import easyocr
from PIL import Image

reader = easyocr.Reader(["en", "es"], gpu=False)


image = cv2.imread("data/test1.png")
image_solved = cv2.imread("data/test1.png")
frame = None
result = reader.readtext(image)
matrix_wordsearch = []
matrix_keywords = []
basis_points = []
compass_matrix = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

found = []
found_reverse = []

horizontal_flag = False
horizontalR_flag = False
vertical_flag = False
verticalR_flag = False
crossright_flag = False
crossrightR_flag = False
crossleft_flag = False
crossleftR_flag = False

points = []

axles = []


aux = []

for res in result:
    pt0, pt1, pt2, pt3 = res[0][0], res[0][1], res[0][2], res[0][3]
    if len(res[1]) > 8:
        for i in res[1]:
            if i != " ":
                if i == "0":
                    aux.append("O")
                elif i == "|" or i == "1" or i == "/":
                    aux.append("I")
                elif i == "$":
                    aux.append("S")
                elif i != i.upper():
                    aux.append(i.upper())
                else:
                    aux.append(i)
        points.append((pt0, pt1, pt2, pt3))
        

        matrix_wordsearch.append(aux)
        aux = []

    elif res[0][0][1] > 800:
        matrix_keywords.append(res[1])


    cv2.rectangle(image, pt0, (pt1[0], pt1[1] - 23), (0, 255, 0), 2)
    cv2.putText(image, res[1], (pt0[0], pt0[1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    cv2.rectangle(image, pt0, pt2, (0, 255, 0), 2)


for row in matrix_wordsearch:
    print(row)


print(matrix_keywords)


for word in matrix_keywords:
    print("Word: ", word)
    for i in range(len(matrix_wordsearch)):
        for j in range(len(matrix_wordsearch[i])):
            if matrix_wordsearch[i][j] == word[0]:
                print("Letter: ", word[0], "position: ", i, j)
                axles.append([i,j])
                for index_letter in range(1,len(word)):
                    if index_letter == 1:
                        if j + index_letter <= len(word) and matrix_wordsearch[i][j + index_letter] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i, j + index_letter)
                            axles.append([i, j + index_letter])
                            horizontal_flag = True
                            print("Horizontal Derecha")
                            print(axles)
                        elif j + index_letter >= len(word) and matrix_wordsearch[i][j - index_letter] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i, j - index_letter)
                            axles.append([i, j - index_letter])
                            horizontalR_flag = True
                            print("Horizontal Izquierda")
                            print(axles)
                        elif i + index_letter >= len(word) and matrix_wordsearch[i - index_letter][j] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i - index_letter, j)
                            axles.append([i - index_letter, j])
                            verticalR_flag = True
                            print("Vertical Arriba")
                            print(axles)
                        elif i + index_letter <= len(word) and matrix_wordsearch[i + index_letter][j] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i + index_letter, j)
                            axles.append([i + index_letter, j])
                            vertical_flag = True
                            print("Vertical Abajo")
                            print(axles)
                        elif i + index_letter <= len(word) and j + index_letter <= len(word) and matrix_wordsearch[i + index_letter][j + index_letter] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i + index_letter, j)
                            axles.append([i + index_letter, j + index_letter])
                            crossright_flag = True
                            print("Cruz Derecha Baja")
                            print(axles)
                        elif i + index_letter >= len(word) and j + index_letter >= len(word) and matrix_wordsearch[i - index_letter][j - index_letter] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i - index_letter, j - index_letter)
                            axles.append([i - index_letter, j - index_letter])
                            crossleftR_flag = True
                            print("Cruz Izquierda Arriba")
                            print(axles)
                        elif i - index_letter >= 0 and j + index_letter <= 6 and matrix_wordsearch[i - index_letter][j + index_letter] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i - index_letter, j + index_letter)
                            axles.append([i - index_letter, j + index_letter])
                            crossrightR_flag = True
                            print("Cruz Derecha Arriba")
                            print(axles)
                        elif i + index_letter <= 6 and j - index_letter >= 0 and matrix_wordsearch[i + index_letter][j - index_letter] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i + index_letter, j - index_letter)
                            axles.append([i + index_letter, j - index_letter])
                            crossleft_flag = True
                            print("Cruz Izquierda Baja")
                            print(axles)

                        else:
                            print("No se encontró la letra", word[index_letter], index_letter, len(word))
                            break
                    else:
                        if horizontal_flag and matrix_wordsearch[i][j + index_letter] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i, j + index_letter)
                            axles.append([i, j + index_letter])
                            print("Horizontal Derecha")
                            print(axles)
                        elif horizontalR_flag and matrix_wordsearch[i][j - index_letter] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i, j - index_letter)
                            axles.append([i, j - index_letter])
                            print("Horizontal Izquierda")
                            print(axles)
                        elif verticalR_flag and matrix_wordsearch[i - index_letter][j] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i - index_letter, j)
                            axles.append([i - index_letter, j])
                            print("Vertical Arriba")
                            print(axles)
                        elif vertical_flag and matrix_wordsearch[i + index_letter][j] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i + index_letter, j)
                            axles.append([i + index_letter, j])
                            print("Vertical Abajo")
                            print(axles)
                        elif crossright_flag and matrix_wordsearch[i + index_letter][j + index_letter] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i + index_letter, j + index_letter)
                            axles.append([i + index_letter, j + index_letter])
                            print("Cruz Derecha Baja")
                            print(axles)
                        elif crossleftR_flag and matrix_wordsearch[i - index_letter][j - index_letter] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i - index_letter, j - index_letter)
                            axles.append([i - index_letter, j - index_letter])
                            print("Cruz Izquierda Arriba")
                            print(axles)
                        elif crossrightR_flag and matrix_wordsearch[i - index_letter][j + index_letter] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i - index_letter, j + index_letter)
                            axles.append([i - index_letter, j + index_letter])
                            print("Cruz Derecha Arriba")
                            print(axles)
                        elif crossleft_flag and matrix_wordsearch[i + index_letter][j - index_letter] == word[index_letter]:
                            print("Letter: ", word[index_letter], "position: ", i + index_letter, j - index_letter)
                            axles.append([i + index_letter, j - index_letter])
                            print("Cruz Izquierda Baja")
                            print(axles)
                        
                        else:
                            print("No se encontró la letra", word[index_letter], index_letter, len(word))
                            break



                if len(axles) == len(word):
                        break
                else:
                    print(axles)
                    axles = []
                    horizontal_flag = False
                    horizontalR_flag = False
                    vertical_flag = False
                    verticalR_flag = False
                    crossright_flag = False
                    crossrightR_flag = False
                    crossleft_flag = False
                    crossleftR_flag = False
                    
        if len(axles) == len(word):
            break
    for axis in axles:
        compass_matrix[axis[0]][axis[1]] = 1
    
    print(axles)

    print("\n")
    for row in compass_matrix:
        print(row)
    print("\n")

    if horizontal_flag:
        cv2.rectangle(image_solved, (points[0][0][0] + 82 * axles[0][1], points[axles[0][0]][0][1]), (points[0][1][0] - 82 * abs(axles[-1][1] - 6), points[axles[-1][0]][2][1]), (0, 0, 255), 2)
        print((points[0][0][0] + 82 * axles[0][1], points[axles[0][0]][0][1]), (points[0][1][0] - 82 * abs(axles[-1][1] - 6), points[axles[-1][0]][2][1]))
    
    if horizontalR_flag:
        cv2.rectangle(image_solved, (points[0][0][0] + 82 * axles[-1][1], points[axles[-1][0]][0][1]), (points[0][1][0] - 82 * abs(axles[0][1] - 6), points[axles[0][0]][2][1]), (0, 0, 255), 2)
        print((points[0][0][0] + 82 * axles[-1][1], points[axles[-1][0]][0][1]), (points[0][1][0] - 82 * abs(axles[0][1] - 6), points[axles[0][0]][2][1]))
    
    if vertical_flag:
        cv2.rectangle(image_solved, (points[0][0][0] + 82 * axles[0][1], points[axles[0][0]][0][1]), (points[0][1][0] - 82 * abs(axles[-1][1] - 6), points[axles[-1][0]][2][1]), (0, 255, 0), 2)
        print((points[0][0][0] + 82 * axles[0][1], points[axles[0][0]][0][1]), (points[0][1][0] - 82 * abs(axles[-1][1] - 6), points[6][2][1] - 70 * abs(axles[-1][0] - 6)))
    
    if verticalR_flag:
        cv2.rectangle(image_solved, (points[0][0][0] + 82 * axles[-1][1], points[axles[-1][0]][0][1]), (points[0][1][0] - 82 * abs(axles[0][1] - 6), points[axles[0][0]][2][1]), (0, 255, 0), 2)
        print((points[0][0][0] + 82 * axles[-1][1], points[axles[-1][0]][0][1]), (points[0][1][0] - 82 * abs(axles[0][1] - 6), points[axles[0][0]][2][1]))
    
    if crossright_flag:
        cv2.line(image_solved, ((points[0][0][0] - 10) + 82 * axles[0][1], points[axles[0][0]][0][1]), ((points[0][0][0] + 40) + 82 * axles[0][1], points[axles[0][0]][0][1]), (255, 0, 0), 3)
        cv2.line(image_solved, ((points[0][0][0] - 10) + 82 * axles[0][1], points[axles[0][0]][0][1]), ((points[0][0][0] - 10) + 82 * axles[0][1], (points[axles[0][0]][2][1] - 20)), (255, 0, 0), 3)

        cv2.line(image_solved, ((points[0][0][0] + 20) + 82 * axles[-1][1], points[axles[-1][0]][2][1]), (points[0][1][0] - 82 * abs(axles[-1][1] - 6), points[axles[-1][0]][2][1]), (255, 0, 0), 2)
        cv2.line(image_solved, (points[0][1][0] - 82 * abs(axles[-1][1] -6), points[axles[-1][0]][2][1]), (points[0][1][0] - 82 * abs(axles[-1][1] - 6), (points[axles[-1][0]][0][1] + 20)), (255,0,0), 3)

        cv2.line(image_solved, (points[0][1][0] - 82 * abs(axles[-1][1] -6), (points[axles[-1][0]][0][1] + 20)), ((points[0][0][0] + 40) + 82 * axles[0][1], points[axles[0][0]][0][1]), (255, 0, 0), 3)
        cv2.line(image_solved, ((points[0][0][0] + 20) + 82 * axles[-1][1], points[axles[-1][0]][2][1]), ((points[0][0][0] - 10) + 82 * axles[0][1], (points[axles[0][0]][2][1] - 20)), (255,0,0), 3)
    
    if crossrightR_flag:
        cv2.line(image_solved, ((points[0][0][0] + 10) + 82 * axles[0][1], points[axles[0][0]][2][1]), ((points[0][0][0] + 30) + 92 * axles[0][1], points[axles[0][0]][2][1]), (255, 0, 0), 3)
        cv2.line(image_solved, ((points[0][0][0] + 10) + 82 * axles[0][1], points[axles[0][0]][2][1]), ((points[0][0][0] + 10) + 82 * axles[0][1], points[axles[0][0]][0][1] + 10), (255, 0, 0), 3)

        cv2.line(image_solved, ((points[0][1][0]) - 82 * abs(axles[-1][1] - 6), points[axles[-1][0]][0][1]), (((points[0][1][0]) - 50) - 82 * abs(axles[-1][1] - 6), points[axles[-1][0]][0][1]), (255, 0, 0), 3)
        cv2.line(image_solved, ((points[0][1][0]) - 82 * abs(axles[-1][1] - 6), points[axles[-1][0]][0][1]), ((points[0][1][0]) - 82 * abs(axles[-1][1] - 6), points[axles[-1][0]][2][1]), (255, 0, 0), 3)

        cv2.line(image_solved, ((points[0][0][0] + 30) + 92 * axles[0][1], points[axles[0][0]][2][1]), ((points[0][1][0]) - 82 * abs(axles[-1][1] - 6), points[axles[-1][0]][2][1]) , (255, 0, 0), 3)
        cv2.line(image_solved, ((points[0][0][0] + 10) + 82 * axles[0][1], points[axles[0][0]][0][1] + 10), (((points[0][1][0]) - 50) - 82 * abs(axles[-1][1] - 6), points[axles[-1][0]][0][1]), (255,0,0), 3)
    
    if crossleft_flag:
        cv2.line(image_solved, ((points[0][0][0] + 10) + 82 * axles[-1][1], points[axles[-1][0]][2][1]), ((points[0][0][0] + 30) + 92 * axles[-1][1], points[axles[-1][0]][2][1]), (255, 0, 0), 3)
        cv2.line(image_solved, ((points[0][0][0] + 10) + 82 * axles[-1][1], points[axles[-1][0]][2][1]), ((points[0][0][0] + 10) + 82 * axles[-1][1], points[axles[-1][0]][0][1] + 10), (255, 0, 0), 3)

        cv2.line(image_solved, ((points[0][1][0]) - 82 * abs(axles[0][1] - 6), points[axles[0][0]][0][1]), (((points[0][1][0]) - 50) - 82 * abs(axles[0][1] - 6), points[axles[0][0]][0][1]), (255, 0, 0), 3)
        cv2.line(image_solved, ((points[0][1][0]) - 82 * abs(axles[0][1] - 6), points[axles[0][0]][0][1]), ((points[0][1][0]) - 82 * abs(axles[0][1] - 6), points[axles[0][0]][2][1]), (255, 0, 0), 3)

        cv2.line(image_solved, ((points[0][0][0] + 30) + 92 * axles[-1][1], points[axles[-1][0]][2][1]), ((points[0][1][0]) - 82 * abs(axles[0][1] - 6), points[axles[0][0]][2][1]) , (255, 0, 0), 3)
        cv2.line(image_solved, ((points[0][0][0] + 10) + 82 * axles[-1][1], points[axles[-1][0]][0][1] + 10), (((points[0][1][0]) - 50) - 82 * abs(axles[0][1] - 6), points[axles[0][0]][0][1]), (255,0,0), 3)
    
    if crossleftR_flag:
        cv2.line(image_solved, ((points[0][0][0] - 10) + 82 * axles[-1][1], points[axles[-1][0]][0][1]), ((points[0][0][0] + 40) + 82 * axles[-1][1], points[axles[-1][0]][0][1]), (255, 0, 0), 3)
        cv2.line(image_solved, ((points[0][0][0] - 10) + 82 * axles[-1][1], points[axles[-1][0]][0][1]), ((points[0][0][0] - 10) + 82 * axles[-1][1], (points[axles[-1][0]][2][1] - 20)), (255, 0, 0), 3)

        cv2.line(image_solved, ((points[0][0][0] + 20) + 82 * axles[0][1], points[axles[0][0]][2][1]), (points[0][1][0] - 82 * abs(axles[0][1] - 6), points[axles[0][0]][2][1]), (255, 0, 0), 2)
        cv2.line(image_solved, (points[0][1][0] - 82 * abs(axles[0][1] -6), points[axles[0][0]][2][1]), (points[0][1][0] - 82 * abs(axles[0][1] - 6), (points[axles[0][0]][0][1] + 20)), (255,0,0), 3)

        cv2.line(image_solved, (points[0][1][0] - 82 * abs(axles[0][1] -6), (points[axles[0][0]][0][1] + 20)), ((points[0][0][0] + 40) + 82 * axles[-1][1], points[axles[-1][0]][0][1]), (255, 0, 0), 3)
        cv2.line(image_solved, ((points[0][0][0] + 20) + 82 * axles[0][1], points[axles[0][0]][2][1]), ((points[0][0][0] - 10) + 82 * axles[-1][1], (points[axles[-1][0]][2][1] - 20)), (255,0,0), 3)

    cv2.imwrite(f"frames/frame{word}.png", image_solved)
    frame = Image.open(f"frames/frame{word}.png")
    width, height = frame.size

    new_image = Image.new('RGB', (width + 600, height), color = 'black')

    new_image.paste(frame, (0,0))

    new_image.save(f"frames/frame{word}.png")

    frame = cv2.imread(f"frames/frame{word}.png")

    cv2.putText(frame, f"Word: {word}", (width + 100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)

    for index_row in range(len(compass_matrix)):
        cv2.putText(frame, str(compass_matrix[index_row]), (width + 50, 300 + (60 * index_row)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

    cv2.imwrite(f"frames/frame{word}.png", frame)

    compass_matrix = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
    ]

    
    axles = []
    horizontal_flag = False
    horizontalR_flag = False
    vertical_flag = False
    verticalR_flag = False
    crossright_flag = False
    crossrightR_flag = False
    crossleft_flag = False
    crossleftR_flag = False
    print("\n")


cv2.imwrite("data/solved.png", image_solved)