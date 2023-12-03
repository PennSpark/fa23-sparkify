export type Track = {
	name: string;
	artists: string[];
	url: string;
	album: Album;
};

export type Album = {
	name: string;
	artists: string[];
	url: string;
	img: string;
};

export type Artist = {
	name: string;
	genres: string[];
	url: string;
	imgs: string[];
};

export type Image = {
	url: string;
	rank: number;
};
