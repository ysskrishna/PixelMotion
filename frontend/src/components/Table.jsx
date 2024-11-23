import React from 'react'
import moment from 'moment';

function isValidData(data) {
    return Array.isArray(data) && data.length > 0;
}

function getRelativeTime(isoDate) {
    return moment(isoDate).fromNow();
}
function Table({data}) {
    // Sort data by created_at in descending order
    const sortedData = [...data].sort((a, b) => 
        new Date(b.created_at) - new Date(a.created_at)
    );

    if (!isValidData(sortedData)) {
        return <></>
    }

    const handleDownload = async (videoUrl) => {
        try {
            const fileName = `video_${Date.now()}.mp4`;

            const response = await fetch(videoUrl);
            if (!response.ok) {
                throw new Error('Failed to download video');
            }

            const blob = await response.blob();
            const objectUrl = URL.createObjectURL(blob);


            const link = document.createElement('a');
            link.href = objectUrl;
            link.download = fileName;

            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            URL.revokeObjectURL(objectUrl);
        } catch (error) {
            console.error('Error downloading video:', error);
        }
    };

    const handleView = (videoUrl) => {
        window.open(videoUrl, '_blank');
    };
    
  return (
    <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
        <table className="table-auto w-full text-sm text-left rtl:text-right text-gray-500">
            <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                <tr>
                    <th scope="col" className="px-6 py-3">
                        Title
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Image
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Progress
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Status Message
                    </th>
                    <th scope="col" className="px-6 py-3">
                        Uploaded At
                    </th>

                    <th scope="col" className="px-6 py-3">
                        Actions
                    </th>
                </tr>
            </thead>
            <tbody>
                {
                    sortedData.map((item, index) => (
                        <tr key={index} className="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700">
                            <th scope="row" className="px-6 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                {item?.title}
                            </th>
                            <td className="px-6 py-3">
                                {item?.image_url && (
                                    <img 
                                        src={item.image_url} 
                                        alt={item.title || 'Preview'} 
                                        className="object-contain w-full max-w-[200px] max-h-[150px]"
                                    />
                                )}
                            </td>
                            <td className="px-6 py-3">
                                <span className="block mb-1 text-sm font-medium">
                                    {item?.status}
                                </span>
                                <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                                    <div 
                                        className="bg-blue-600 h-2.5 rounded-full transition-all duration-300" 
                                        style={{ width: `${item?.progress || 0}%` }}
                                    >
                                    </div>
                                </div>
                                <span className="text-xs mt-1 block">{item?.progress || 0}%</span>
                            </td>
                            <td className="px-6 py-3">
                                {item?.message}
                            </td>
                            <td className="px-6 py-3">
                                {getRelativeTime(item?.created_at)}
                            </td>
                            <td className="px-6 py-3">
                                {item?.status === 'success' && (
                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => handleView(item?.video_url)}
                                            className="p-2 text-blue-600 dark:text-blue-500 hover:bg-blue-100 dark:hover:bg-blue-900 rounded-full"
                                            title="View Video"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                                                <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                                                <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                            </svg>
                                        </button>
                                        <button
                                            onClick={() => handleDownload(item?.video_url)}
                                            className="p-2 text-blue-600 dark:text-blue-500 hover:bg-blue-100 dark:hover:bg-blue-900 rounded-full"
                                            title="Download Video"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                                                <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                                            </svg>
                                        </button>
                                    </div>
                                )}
                            </td>
                        </tr>
                    ))
                }
            </tbody>
        </table>
    </div>
  )
}

export default Table