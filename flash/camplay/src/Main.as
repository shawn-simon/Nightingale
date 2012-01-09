package
{
	import flash.display.Sprite;
	import flash.display.StageScaleMode;
	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.NetStatusEvent;
	import flash.events.IOErrorEvent;
	import flash.events.SecurityErrorEvent;
	import flash.events.AsyncErrorEvent;
	import flash.media.Camera;
	import flash.media.Video;
	import flash.media.Microphone;
	import flash.net.NetConnection;
	import flash.net.NetStream;
	import flash.net.ObjectEncoding;
	import flash.text.TextField;

	[SWF(width=320, height=240, frameRate=30)]
	public class Main extends Sprite 
	{
		//private var streamUrl:String = "rtmp://107.21.119.80:1935/myapp";
		private var streamUrl:String = "rtmp://localhost:1935/myapp";
		private var streamName:String = "kevin";
		private var nc:NetConnection;
		private var ns:NetStream;
		private var debugText:String = "";
		
		public const WIDTH:uint = 320;
		public const HEIGHT:uint = 240;
		
		public function Main():void 
		{
			if (stage)
			{
				init();
			}
			else 
			{
				addEventListener(Event.ADDED_TO_STAGE, init);
			}
		}
		
		private function init(e:Event = null):void 
		{
			removeEventListener(Event.ADDED_TO_STAGE, init);
			stage.scaleMode = StageScaleMode.NO_BORDER;
		
			connect();
		}
		
		private function connect():void
		{
			//NetConnection.defaultObjectEncoding = ObjectEncoding.AMF0;
			NetConnection.defaultObjectEncoding = ObjectEncoding.AMF3;
			
			if (nc == null)
			{
				nc = new NetConnection();
				nc.addEventListener(NetStatusEvent.NET_STATUS, netStatusHandler, false, 0, true);
				nc.addEventListener(IOErrorEvent.IO_ERROR, errorHandler, false, 0, true);
				nc.addEventListener(SecurityErrorEvent.SECURITY_ERROR, errorHandler, false, 0, true);
				nc.addEventListener(AsyncErrorEvent.ASYNC_ERROR, errorHandler, false, 0, true);
				nc.client = {};
				debug('connect() ' + streamUrl);
				nc.connect(streamUrl);
			}
		}
		
		private function playstream():void
		{
			if (ns == null && nc != null && nc.connected)
			{
				ns = new NetStream(nc);
				ns.addEventListener(NetStatusEvent.NET_STATUS, netStatusHandler, false, 0, true);
				ns.addEventListener(IOErrorEvent.IO_ERROR, streamErrorHandler, false, 0, true);
				ns.addEventListener(AsyncErrorEvent.ASYNC_ERROR, streamErrorHandler, false, 0, true);
				ns.bufferTime = 0.4;
				ns.client = {};
				ns.play(streamName, -1);
				createLocalCamera();
			}
			else
			{
				debug("unable to play stream");
				debug(ns == null);
				debug(nc != null);
				debug(nc.connected);
			}
			var txtDebug:TextField = new TextField();
			txtDebug.width = 400;
			txtDebug.height = 400;
			txtDebug.text = debugText;
			addChild(txtDebug);
		}
		
		private function createLocalCamera():void
		{
			var video:Video = new Video(WIDTH, HEIGHT);
			video.smoothing = true;
			//video.deblocking = 0;
			video.attachNetStream(ns);
			addChild(video);
			debug("video.smoothing " + video.smoothing);
			debug("video.deblocking " + video.deblocking);
		}
		
		private function netStatusHandler(event:NetStatusEvent):void
		{
			debug('netStatusHandler() ' + event.type + ' ' + event.info.code);
			switch(event.info.code)
			{
				case 'NetConnection.Connect.Success':
					playstream();
					break;
				case 'NetConnection.Connect.Failed':
				case 'NetConnection.Connect.Reject':
				case 'NetConnection.Connect.Closed':
					nc = null;
					closeStream();
					break;
			}
		}
		
		private function errorHandler(event:ErrorEvent):void
		{
			debug('errorHandler() ' + event.type + ' ' + event.text);
			if (nc != null)
			{
				nc.close();
			}
			nc = null;
			closeStream();
		}
		
		private function streamErrorHandler(event:ErrorEvent):void
		{
			debug('streamErrorHandler() ' + event.type + ' ' + event.text);
			closeStream();
		}
		
		private function closeStream():void
		{
			if (ns != null)
			{
				ns.close();
				ns = null;
			}
		}
		
		private function debug(msg:Object):void
		{
			debugText += msg + "\n";
		}
	}
}