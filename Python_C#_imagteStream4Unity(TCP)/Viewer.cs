using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace HD
{
    public class Viewer : MonoBehaviour
    {
        public RawImage rawimage;
        public AspectRatioFitter fit;

        #region Data
        public static Viewer instance;
        private byte[] imageToDisplay;
        #endregion

        #region Get Set
        public void SetImageToDisplay(byte[] image)
        {
            instance.imageToDisplay = image;
        }
        #endregion

        #region API
        internal static void DisplayImage(byte[] image)
        {
            if (image == null)
                return;
            if (image.Length > 0)
            {
                //이미지 크기 생성 이후 streaming 되는 이미지 크기에 맞게 수정 해야함
                Texture2D texture = new Texture2D(910, 664);
                //byte형식의 데이터를 texture2D 형식으로 읽음
                texture.LoadImage(image);
                //이미지를 화면에 입힘(Canvas 아래 RawImage)
                instance.rawimage.texture = texture as Texture;
                //이미지 가로 세로 비율
                instance.fit.aspectRatio = 910/664;
            }
        }
        #endregion
        // Start is called before the first frame update
        void Awake()
        {
            instance = this;
        }

        // Update is called once per frame
        void Update()
        {
            DisplayImage(instance.imageToDisplay);
        }
    }
}