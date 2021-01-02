void ButtonShow(void){
	int i;
 
	for(i=0; i< buttonNum; i++){
		if(i != 0){
			L_width = buttonAddr[i-1][2] + 30;
		}
		b_seat1=drawButton(img, buttonName[i],Point(L_width, L_height),0);
		buttonAddr[i] = (int *)malloc(4);
 
		buttonAddr[i][0] = b_seat1.x;
		buttonAddr[i][1] = b_seat1.y;
		buttonAddr[i][2] = b_seat1.width + b_seat1.x;
		buttonAddr[i][3] = b_seat1.height+ b_seat1.y;
	}
}

//将用户鼠标左键按下和抬起的坐标都保存在tmpAddr，接着使用函数choiceButton和on_button进行控件的选择和响应。
void on_mouse( int event, int x, int y, int flags, void* ustc)  
{
	int buttonNow = -3;
	if(event == CV_EVENT_LBUTTONDOWN){
		tmpAddr[0] = x;
		tmpAddr[1] = y;
		tmpAddr[2] = 0;
		tmpAddr[3] = 0;
	}else if(event == CV_EVENT_LBUTTONUP){
		tmpAddr[2] = x;
		tmpAddr[3] = y;
		buttonNow = choiceButton(tmpAddr, buttonAddr, buttonNum);
		on_button(buttonNow);
	}
}

/*在鼠标左键抬起的时候调用函数：choiceButton。
       tmpAddr：鼠标左键按下时候的坐标和鼠标左键抬起时候的坐标。
       buttonAddr： 控件的个数和它们的坐标信息。
       size：控件的数量。
　　在choiceButton中，1、判断鼠标按下和抬起的坐标是不是在同一个位置，不是的话就直接返回-2。
                    2、判断鼠标左键按下的坐标是不是在控件的范围之类，是的话，就直接返回控件编号。
                    3、如果鼠标左键按下的位置没有在任何一个控件范围内，返回 -1。*/
int choiceButton(int* tmpAddr, int** buttonAddr, int size){
	int i, tmp;
 
	tmp = abs(tmpAddr[0] - tmpAddr[2]) + abs(tmpAddr[1] - tmpAddr[3]);
	if(tmp > 20){
		return -2;	
	}
	for(i=0; i< size; i++){
		if((buttonAddr[i][0] < tmpAddr[0]) && (buttonAddr[i][2] > tmpAddr[0])){
			if((buttonAddr[i][1] < tmpAddr[1]) && (buttonAddr[i][3] > tmpAddr[3])){
				return i;
			}
		}
	}
	return -1;
}

//根据前面控件选择传回来的参数，对应的用该参数作为空白图片的显示窗口名字，并显示出来。
void on_button(int buttonNow){
	char str[20];
	sprintf(str,"%d", buttonNow);
	Mat img = cv::Mat(300, 300, CV_8UC3, 1);
	imshow(str, img);
}

/*　　首先加载一副图片作为背景图，接着将使用ButtonShow将button画在背景图片上，同时将每个button的坐标位置都保存在buttonAddr数组中，接着将
画好button之后的背景图片显示出来，最后给该背景图加上鼠标响应和等待用户操作。*/
int main(int argc,char **argv){
	img=imread(back_name,1);

	ButtonShow();
	imshow(back_show, img);
	cvSetMouseCallback(back_show, on_mouse, NULL);
	waitKey();
}

/*按下控件：cancel，弹出窗口0。
　　按下控件：add， 弹出窗口1。*/