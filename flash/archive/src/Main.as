package 
{
	import flash.display.SimpleButton;
	import flash.display.Sprite;
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
	
	public class Main extends Sprite 
	{
		//private var streamUrl:String = "rtmp://107.21.119.80:1935/myapp";
		private var streamUrl:String = "rtmp://localhost:1935/myapp";
		private var streamName:String = "stream1";
		private var nc:NetConnection;
		private var ns:NetStream;
		private var debugText:TextField;
		
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
			
			debugText = new TextField();
			debugText.width = 400;
			debugText.height = 400;
			addChild(debugText);
			
			createLocalCamera();
			connect();
		}
		
		private function connect():void
		{
        	NetConnection.defaultObjectEncoding = ObjectEncoding.AMF0; // MUST SUPPLY THIS!!!
			
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
		
		private function publish():void
		{
        	if (ns == null && nc != null && nc.connected)
			{
        		ns = new NetStream(nc);
        		ns.addEventListener(NetStatusEvent.NET_STATUS, netStatusHandler, false, 0, true);
        		ns.addEventListener(IOErrorEvent.IO_ERROR, streamErrorHandler, false, 0, true);
        		ns.addEventListener(AsyncErrorEvent.ASYNC_ERROR, streamErrorHandler, false, 0, true);
        		ns.client = {};
        		
        		ns.publish(streamName, 'record');
        		ns.attachCamera(Camera.getCamera());
        		ns.attachAudio(Microphone.getMicrophone( -1));
        	}
			else
			{
				debug("unable to publish stream");
				debug(ns == null);
				debug(nc != null);
				debug(nc.connected);
			}
		}
		
		private function createLocalCamera():void
		{
			var video:Video = new Video(640/2, 480/2);
			var camara:Camera = Camera.getCamera();
			camara.setMode(640/2, 480/2, 30);
			video.attachCamera(camara);
			video.x = 300;
			addChild(video);
		}
		
        private function netStatusHandler(event:NetStatusEvent):void
		{
        	debug('netStatusHandler() ' + event.type + ' ' + event.info.code);
        	switch(event.info.code)
			{
				case 'NetConnection.Connect.Success':
					publish();
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
			debugText.appendText(msg + "\n");
		}
	}
}